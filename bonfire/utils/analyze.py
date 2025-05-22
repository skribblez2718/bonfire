from __future__ import annotations

import json
import os
import re
import ssl
import time
from typing import Any, Dict, Optional, Tuple

import httpx
from httpx import HTTPError
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from pydantic import ValidationError

from bonfire.utils.prompt import SYSTEM_PROMPT, USER_PROMPT
from bonfire.utils.validate import BonfireResponseModel

MAX_RETRIES: int = 3
BACKOFF_BASE: int = 2
TIMEOUT: int = 120
TEMPERATURE: float = 0.2
TOP_P: float = 0.9


###################################[  start BonfireAnalyze  ]###################################
class BonfireAnalyze:
    """
    LLM-backed analyser supporting OpenAI-compatible, Azure OpenAI and Ollama models
    with optional private-CA trust, structured-output enforcement and resilient
    retry logic.
    """

    #########################[  start send_request  ]#########################
    @staticmethod
    def send_request(
        obj: Dict[str, Any], logger: "Logger"
    ) -> Optional[BonfireResponseModel]:
        """
        Build the chat prompt, route it to the chosen provider, and return a
        validated :class:`BonfireResponseModel`.

        Retries *content-filter*, validation and network errors with exponential
        back-off (``MAX_RETRIES``).

        Args:
            obj: Dict containing ``intent``, ``prompt`` and ``response`` fields.
            logger: App-level logger (debug/info/warn/error).

        Returns:
            A validated response model **or** a fallback instance with
            ``result="unknown"`` and ``reason`` explaining the failure.
            ``None`` is returned only on unexpected fatal errors.
        """
        prompt_body: str = BonfireAnalyze._build_prompt(obj)
        provider: str = os.getenv("PROVIDER").lower()

        # Build once – reused for every retry / provider call
        httpx_client: httpx.Client = BonfireAnalyze._build_httpx_client()

        provider_fn_map: Dict[str, Tuple] = {
            "openai": (BonfireAnalyze._call_openai, (prompt_body, httpx_client)),
            "azure_openai": (BonfireAnalyze._call_azure_openai, (prompt_body,)),
            "ollama": (BonfireAnalyze._call_ollama, (prompt_body, httpx_client)),
        }
        if provider not in provider_fn_map:
            logger.error(f"Unknown {provider} provider – aborting analysis")
            return None

        call_fn, fn_args = provider_fn_map[provider]

        json_str: Optional[str] = BonfireAnalyze._invoke_with_retry(
            fn=call_fn,
            fn_args=fn_args,
            logger=logger,
            max_retries=MAX_RETRIES,
        )

        if json_str is None:  # all retries failed
            reason = "Model was unable to analyze the result likley due to network issues and/or invalid responses"
            fallback_response = BonfireAnalyze._fallback_response(reason=reason)
            obj["result"] = getattr(fallback_response, "result", None)
            obj["reason"] = getattr(fallback_response, "reason", None)
            return obj

        try:
            model_dict: Dict[str, Any] = json.loads(json_str)
            response_model = BonfireResponseModel(**model_dict)
            obj["result"] = getattr(response_model, "result", None)
            obj["reason"] = getattr(response_model, "reason", None)
            return obj
        except (json.JSONDecodeError, ValidationError) as exc:
            logger.error(f"Validation/JSON error after successful call: {exc}")
            fallback_response = BonfireAnalyze._fallback_response(
                reason="validation-error"
            )
            obj["result"] = getattr(fallback_response, "result", None)
            obj["reason"] = getattr(fallback_response, "reason", None)
            return obj

    #########################[  end send_request  ]###########################

    #########################[  start _build_prompt  ]########################
    @staticmethod
    def _build_prompt(obj: Dict[str, Any]) -> str:
        """Return the final user prompt injected into the template."""
        intent = obj.get("intent", "").replace("_", " ").title()
        prompt = obj.get("prompt", "")
        response_text = obj.get("response", "")
        return USER_PROMPT.format(
            intent=intent,
            prompt=prompt,
            response_text=response_text,
        )

    #########################[  end _build_prompt  ]##########################

    #########################[  start _build_httpx_client  ]##################
    @staticmethod
    def _build_httpx_client() -> httpx.Client:
        """
        Build a shared ``httpx.Client``.

        * Uses ``CERT_PATH`` env-var if present to extend trust store.
        * Disables proxy / trust-env inheritance for deterministic behaviour.
        """
        cert_path: Optional[str] = os.getenv("CERT_PATH")
        ssl_ctx = (
            ssl.create_default_context(cafile=cert_path)
            if cert_path
            else ssl.create_default_context()
        )
        return httpx.Client(
            verify=ssl_ctx, timeout=TIMEOUT, trust_env=False
        )  # verify accepts an SSLContext:contentReference[oaicite:2]{index=2}

    #########################[  end _build_httpx_client  ]###################

    #########################[  start _invoke_with_retry  ]##################
    @staticmethod
    def _invoke_with_retry(
        fn, fn_args: Tuple[Any, ...], logger: "Logger", max_retries: int = 3
    ) -> Optional[str]:
        """
        Generic retry wrapper for provider calls.

        Returns the provider’s raw JSON string or ``None`` if all attempts fail.
        Retries network/timeout-like errors across OpenAI, Azure and httpx.
        """
        for attempt in range(max_retries):
            try:
                return fn(*fn_args)
            except (
                HTTPError,
                TimeoutError,
            ) as net_exc:
                delay = BACKOFF_BASE ** (attempt + 1)
                logger.warning(f"Network error: {net_exc!s}. Retrying in {delay}s…")
            except ValidationError as val_exc:
                delay = BACKOFF_BASE ** (attempt + 1)
                logger.warning(f"Validation error: {val_exc!s}. Retrying in {delay}s…")
            except Exception as exc:  # truly unexpected
                logger.error(f"Fatal, non-retryable error: {exc}")
                break
            time.sleep(delay)
        return None

    #########################[  end _invoke_with_retry  ]####################

    #########################[  start _extract_json  ]#######################
    _JSON_RE = re.compile(r"\{.*?\}", re.DOTALL)

    @classmethod
    def _extract_json(cls, raw: str) -> str:
        """
        Extract the *first* ``{…}`` block.  If none is found, return the original
        string (raises later during validation).
        """
        # Remove possible Markdown code-fences
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
        match = cls._JSON_RE.search(cleaned)
        return match.group() if match else cleaned

    #########################[  end _extract_json  ]#########################

    #########################[  start _call_openai  ]########################
    @staticmethod
    def _call_openai(prompt_body: str, client: httpx.Client) -> str:
        """
        Open-WebUI / any OpenAI-compatible endpoint via ``ChatOpenAI``.
        """
        llm = ChatOpenAI(
            model_name=os.getenv("OPENAI_COMPATIBLE_MODEL"),
            openai_api_base=os.getenv("OPENAI_COMPATIBLE_BASE_URL"),
            openai_api_key=os.getenv("OPENAI_COMPATIBLE_API_KEY"),
            request_timeout=TIMEOUT,
            http_client=client,  # custom SSL / CA bundle support in LangChain:contentReference[oaicite:3]{index=3}
        )
        messages = [("system", SYSTEM_PROMPT), ("human", prompt_body)]
        ai_msg: AIMessage = llm.invoke(messages)
        return BonfireAnalyze._extract_json(ai_msg.content)

    #########################[  end _call_openai  ]##########################

    #########################[  start _call_azure_openai  ]##################
    @staticmethod
    def _call_azure_openai(prompt_body: str) -> str:
        """
        Azure OpenAI via ``AzureChatOpenAI`` (LangChain).
        """
        llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("AZURE_OPENAI_VERSION"),
            openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=TEMPERATURE,
            top_p=TOP_P,
        )
        messages = [("system", SYSTEM_PROMPT), ("human", prompt_body)]
        ai_msg: AIMessage = llm.invoke(messages)
        return BonfireAnalyze._extract_json(ai_msg.content)

    #########################[  end _call_azure_openai  ]####################

    #########################[  start _call_ollama  ]########################
    @staticmethod
    def _call_ollama(prompt_body: str, client: httpx.Client) -> str:
        """
        Local / remote Ollama server via ``ChatOllama``.
        """
        llm = ChatOllama(
            base_url=os.getenv("OLLAMA_BASE_URL"),
            model=os.getenv("OLLAMA_MODEL"),
            temperature=TEMPERATURE,
            top_p=TOP_P,
            http_client=client,  # ChatOllama inherits http_client kw-arg support:contentReference[oaicite:5]{index=5}
            format="json",  # helps coax pure-JSON answers when model supports it
        )
        messages = [("system", SYSTEM_PROMPT), ("human", prompt_body)]
        ai_msg: AIMessage = llm.invoke(messages)
        return BonfireAnalyze._extract_json(ai_msg.content)

    #########################[  end _call_ollama  ]##########################

    #########################[  start _fallback_response  ]##################
    @staticmethod
    def _fallback_response(reason: str) -> BonfireResponseModel:
        """Return a uniform fallback response with an explanatory reason."""
        return BonfireResponseModel(result="unknown", reason=reason)

    #########################[  end _fallback_response  ]####################


###################################[  End BonfireAnalyze  ]#####################################

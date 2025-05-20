import os
import sys

from pydantic import BaseModel, validator
from typing import Optional


###################################[ start BonfireResponseModel ]###################################
class BonfireResponseModel(BaseModel):
    """
    Model for validating LLM response.
    The response must be a JSON with keys "result" (either "pass" or "fail")
    and "reason" (providing information about the outcome).
    """

    result: str
    reason: str

    @validator("result")
    def valid_result(cls, v: str) -> str:
        """
        Validates that the result is either 'pass' or 'fail'.
        """
        if v not in {"pass", "fail", "unknown"}:
            raise ValueError("result must be either 'pass' or 'fail' or 'unknown'")
        return v


###################################[ end BonfireResponseModel ]#####################################


class BonfireValidate:
    """
    Class for validating config and other values.
    """

    #########################[ start validate_env_var ]############################
    @staticmethod
    def _validate_env_var(env_var_name: str, logger: "BonfireLogger") -> Optional[str]:
        """
        Validates that an environment variable is set.

        Args:
            env_var_name: Name of the environment variable to check

        Returns:
            Optional[str]: Value of the environment variable if set, None otherwise
        """
        env_var_value = os.getenv(env_var_name)
        if not env_var_value:
            logger.error(f"{env_var_name} environment variable not set.")
            return None
        return env_var_value

    #########################[ end validate_env_var ]##############################

    #########################[ start validate_env_vars ]###########################
    @staticmethod
    def validate_env_vars(logger: "BonfireLogger") -> bool:
        """
        Validates that all required environment variables are set.

        Returns:
            bool: True if all environment variables are set, False otherwise
        """
        required_env_vars = [
            "BOOTSTRAP_CDN_URL",
            "BOOTSTRAP_JS_CDN_URL",
        ]

        provider = BonfireValidate._validate_env_var("PROVIDER", logger)
        if not provider:
            logger.error(
                "PROVIDER environment variable not set. Must be one of openai, azure_openai, or ollama."
            )

        if provider.lower() == "openai":
            required_env_vars.extend(
                [
                    "OPENAI_COMPATIBLE_MODEL",
                    "OPENAI_COMPATIBLE_BASE_URL",
                    "OPENAI_COMPATIBLE_API_KEY",
                ]
            )
        elif provider.lower() == "azure_openai":
            required_env_vars.extend(
                [
                    "AZURE_OPENAI_ENDPOINT",
                    "AZURE_OPENAI_VERSION",
                    "AZURE_OPENAI_DEPLOYMENT_NAME",
                    "AZURE_OPENAI_API_KEY",
                ]
            )
        elif provider.lower() == "ollama":
            required_env_vars.extend(
                [
                    "OLLAMA_BASE_URL",
                    "OLLAMA_MODEL",
                ]
            )
        else:
            logger.error(
                "Invalid provider. Must be one of 'openai', 'azure_openai', or 'ollama'."
            )
            sys.exit(1)

        for env_var in required_env_vars:
            if not BonfireValidate._validate_env_var(env_var, logger):
                sys.exit(1)

    #########################[ end validate_env_vars ]#############################

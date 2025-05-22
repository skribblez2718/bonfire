from __future__ import annotations

import os
import sys
from typing import Dict, List, Optional

from bonfire.utils.logger import BonfireLogger
from bonfire.utils.text import BonfireTextEvasion
from bonfire.utils.audio import BonfireAudioEvasion
from bonfire.utils.vision import BonfireVisionEvasion
from bonfire.utils.file import BonfireFile


###################################[ start BonfirePayloads ]###################################
class BonfirePayloads:
    """
    Stateless helpers for creating augmented payloads.

    Only :pyfunc:`generate` is part of the **public** surface. All other helpers
    are private (prefixed with ``_``) and should not be accessed directly.
    """

    #########################[ start generate ]#########################
    @staticmethod
    def generate(
        logger: BonfireLogger,
        templates_dir: str,
        available_methods: List[str],
        methods: str,
        output_dir: str,
        data_type: str,
        fmt: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """
        Generate augmented payloads and save them to *output_dir*.

        Args:
            logger: Active :class:`BonfireLogger`.
            templates_dir: Directory where template ``*.jsonl`` files live.
            available_methods: All detected augmentation methods.
            methods: Raw CLI value for ``--methods`` (e.g. ``"all"`` or ``"logical_bypass,role_play"``).
            output_dir: Destination folder for generated ``*.jsonl`` files.
            data_type: ``"text"``, ``"audio"``, or ``"image"``.
            fmt: Optional format hint for audio/image (e.g. ``"mp3"`` or ``"png"``).
        """
        intents_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "intents.jsonl"
        )
        instructions = BonfirePayloads._load_jsonl_file(intents_path, logger)

        chosen = BonfirePayloads._parse_methods_arg(methods, available_methods, logger)
        templates = BonfirePayloads._load_templates(chosen, templates_dir, logger)
        merged_prompts = BonfirePayloads._merge_prompts(instructions, templates)
        intent_groups = BonfirePayloads._group_by_intent(merged_prompts)

        os.makedirs(output_dir, exist_ok=True)

        all_results: List[Dict[str, str]] = []
        intent_file_paths: Dict[str, str] = {}

        if data_type == "text":
            for intent, prompts in intent_groups.items():
                out_file = os.path.join(output_dir, "bonfire_text_payloads.jsonl")
                intent_file_paths[intent] = out_file
                all_results.extend(
                    BonfireTextEvasion(prompts, out_file).generate(logger)
                )
        elif data_type == "audio":
            fmt = BonfirePayloads._validate_format(
                fmt=fmt,
                allowed=["wav", "mp3"],
                default="mp3",
                logger=logger,
                kind="audio",
            )
            for intent, prompts in intent_groups.items():
                out_file = os.path.join(output_dir, "bonfire_audio_payloads.jsonl")
                intent_file_paths[intent] = out_file
                all_results.extend(
                    BonfireAudioEvasion(prompts, out_file, format=fmt).generate(logger)
                )
        elif data_type == "image":
            fmt = BonfirePayloads._validate_format(
                fmt=fmt,
                allowed=["jpeg", "png", "gif"],
                default="png",
                logger=logger,
                kind="image",
            )
            for intent, prompts in intent_groups.items():
                out_file = os.path.join(output_dir, "bonfire_image_payloads.jsonl")
                intent_file_paths[intent] = out_file
                all_results.extend(
                    BonfireVisionEvasion(
                        prompts=prompts, output_file_path=out_file, format=fmt
                    ).generate(logger)
                )
        else:
            logger.error(
                f"Unsupported data_type '{data_type}'. Expected text, audio, or image."
            )
            sys.exit(1)

        BonfirePayloads._log_statistics(all_results, intent_file_paths, logger)

        return all_results

    #########################[ end generate ]###########################

    #########################[ start _parse_methods_arg ]###############
    @staticmethod
    def _parse_methods_arg(
        raw_methods: str, available: List[str], logger: BonfireLogger
    ) -> List[str]:
        cleaned = raw_methods.lower().replace(" ", "")
        available_normalized = [m.lower().replace(" ", "") for m in available]
        chosen = available if cleaned == "all" else [m for m in cleaned.split(",") if m]
        bad = [
            m for m in chosen if m.lower().replace(" ", "") not in available_normalized
        ]
        if bad:
            logger.error(f"Unknown method(s): {', '.join(bad)}")
            sys.exit(1)

        return available if set(chosen) == set(available) else chosen

    #########################[ end _parse_methods_arg ]#################

    #########################[ start _load_jsonl_file ]#################
    @staticmethod
    def _load_jsonl_file(path: str, logger: BonfireLogger) -> List[Dict[str, str]]:
        if not os.path.exists(path):
            logger.error(f"File not found: {path}")
            sys.exit(1)
        try:
            data = BonfireFile.load(path)
            logger.info(f"Loaded {len(data)} records from {path}")
            return data
        except Exception as exc:  # pragma: no cover
            logger.error(f"Error reading {path}: {exc}")
            sys.exit(1)

    #########################[ end _load_jsonl_file ]###################

    #########################[ start _load_templates ]##################
    @staticmethod
    def _load_templates(
        methods: List[str], templates_dir: str, logger: BonfireLogger
    ) -> List[Dict[str, str]]:
        templates: List[Dict[str, str]] = []
        for method in methods:
            fp = os.path.join(templates_dir, f"{method}.jsonl")
            tpl_list = BonfirePayloads._load_jsonl_file(fp, logger)
            for tpl in tpl_list:
                tpl["method_file"] = method
            templates.extend(tpl_list)
        return templates

    #########################[ end _load_templates ]####################

    #########################[ start _merge_prompts ]###################
    @staticmethod
    def _merge_prompts(
        instructions: List[Dict[str, str]], templates: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        merged: List[Dict[str, str]] = []
        for ins in instructions:
            for tpl in templates:
                prompt_val = ins.get("prompt", "")
                # If prompt is a list, handle as multi-turn
                if isinstance(prompt_val, list):
                    # First item is injected, rest are appended as is
                    injected = tpl["template"].replace(
                        "[INSTRUCTIONS]", prompt_val[0] if prompt_val else ""
                    )
                    merged_prompt = [injected] + prompt_val[1:]
                else:
                    merged_prompt = tpl["template"].replace(
                        "[INSTRUCTIONS]", prompt_val
                    )
                merged.append(
                    {
                        "intent": ins.get("intent", ""),
                        "method": tpl["method_file"],
                        "method_name": tpl.get("method", ""),
                        "prompt_name": ins.get("prompt_name", ""),
                        "prompt": merged_prompt,
                    }
                )
        return merged

    #########################[ end _merge_prompts ]#####################

    #########################[ start _group_by_intent ]#################
    @staticmethod
    def _group_by_intent(
        prompts: List[Dict[str, str]],
    ) -> Dict[str, List[Dict[str, str]]]:
        buckets: Dict[str, List[Dict[str, str]]] = {}
        for item in prompts:
            buckets.setdefault(item.get("intent", "unknown"), []).append(item)
        return buckets

    #########################[ end _group_by_intent ]###################

    #########################[ start _validate_format ]#################
    @staticmethod
    def _validate_format(
        *,
        fmt: Optional[str],
        allowed: List[str],
        default: str,
        logger: BonfireLogger,
        kind: str,
    ) -> str:
        fmt = fmt or default
        if fmt not in allowed:
            logger.error(
                f"Invalid format '{fmt}' for {kind}. Must be one of: {', '.join(allowed)}."
            )
            sys.exit(1)
        logger.info(f"Using {kind} format: {fmt}")
        return fmt

    #########################[ end _validate_format ]###################

    #########################[ start _log_statistics ]##################
    @staticmethod
    def _log_statistics(
        results: List[Dict[str, str]], paths: Dict[str, str], logger: BonfireLogger
    ) -> None:
        if not results:
            logger.warning("No results generated – nothing to summarise.")
            return

        counts: Dict[str, Dict[str, int]] = {}
        for res in results:
            intent = res.get("intent", "unknown")
            method = res.get("method", "unknown")
            counts.setdefault(intent, {}).setdefault(method, 0)
            counts[intent][method] += 1

        for intent, methods in counts.items():
            logger.info(f"Intent '{intent}' output saved to: {paths.get(intent)}")
            for method, qty in methods.items():
                logger.info(f"  - {qty} payloads generated using '{method}'")

    #########################[ end _log_statistics ]####################


###################################[ end BonfirePayloads ]#####################################

import os
from typing import List, Dict, Any, Callable, Optional
from bonfire.utils.file import BonfireFile

###################################[ start BonfireResult ]##############################################
class BonfireResult:
    """
    Utility class for grouping and saving results by intent.
    """

    #########################[ start save_by_intent ]##############################################
    @staticmethod
    def save_by_intent(
        results: List[Dict[str, Any]],
        output_dir: str,
        filename_format: str,
        logger,
        post_process: Optional[Callable[[List[Dict[str, Any]], str, str, Any], None]] = None
    ) -> None:
        """
        Groups results by 'intent' and saves each group to a file using the provided filename format.
        Optionally calls post_process for each intent.

        Args:
            results: List of result dicts.
            output_dir: Directory to save files.
            filename_format: Format string for filename, should accept intent as a keyword (e.g. bonfire_{data_type}_analysis_{intent}.jsonl)
            logger: Logger instance.
            post_process: Optional callback for further processing (e.g. HTML report). Signature: (intent_results, file_path, intent, logger)
        """
        results_by_intent = {}
        for res in results:
            intent = res.get("intent", "unknown")
            if intent not in results_by_intent:
                results_by_intent[intent] = []
            results_by_intent[intent].append(res)
        for intent, intent_results in results_by_intent.items():
            file_path = os.path.join(output_dir, filename_format.format(intent=intent))
            BonfireFile.save(intent_results, file_path)
            logger.info(f"Results for intent '{intent}' saved to: {file_path}")
            if post_process:
                post_process(intent_results, file_path, intent, logger)

    #########################[ end save_by_intent ]##############################################

#########################[ end BonfireResult ]################################################



import os

from bonfire.utils.file import BonfireFile
from bonfire.utils.result import BonfireResult


###################################[ start BonfireReport ]###################################
class BonfireReport:
    """
    Class for generating reports from Bonfire analysis results.
    """

    #########################[ start generate ]#########################
    @staticmethod
    def generate(
        analysis_jsonl_path: str, output_dir: str, logger: "BonfireLogger"
    ) -> None:
        """
        Given an analysis JSONL file, generate both HTML and JSONL report files for each intent.
        Report files are named like the analysis file but with _report appended before the extension, and are always saved to output_dir.

        Args:
            analysis_jsonl_path: Path to the analysis JSONL file
            output_dir: Directory to save the report files
            logger: BonfireLogger instance for logging messages
        """
        results = BonfireFile.load(analysis_jsonl_path)
        if not results:
            logger.warning(
                f"No results found in {analysis_jsonl_path}. Skipping report generation."
            )
            return
        # Group by intent if present
        # Extract type (data_type) and use new naming convention
        base, ext = os.path.splitext(os.path.basename(analysis_jsonl_path))
        # Expecting something like bonfire_{type}_analysis_{intent}.jsonl
        parts = base.split("_")
        if len(parts) >= 3 and parts[0] == "bonfire":
            data_type = parts[1]
        else:
            data_type = "unknown"

        #########################[ start post_process ]##############################################
        def post_process(intent_results, file_path, intent, logger):
            # Save JSONL report in the same directory as file_path (intent directory)
            report_base, _ = os.path.splitext(os.path.basename(file_path))
            report_jsonl_path = os.path.join(
                os.path.dirname(file_path), f"{report_base}.jsonl"
            )
            BonfireFile.save(intent_results, report_jsonl_path)

            # Save HTML report in the same directory as file_path (intent directory)
            report_html_path = os.path.join(
                os.path.dirname(file_path), f"{report_base}.html"
            )
            BonfireFile.generate_html_report(intent_results, report_html_path, logger)
            logger.info(
                f"Generated report files: {report_jsonl_path}, {report_html_path}"
            )

        #########################[ end post_process ]################################################

        BonfireResult.save_by_intent(
            results,
            output_dir,
            filename_format=f"bonfire_{data_type}_report_{{intent}}{ext}",
            logger=logger,
            post_process=post_process,
        )

    #########################[ end generate ]###########################


#########################[ end BonfireReport ]################################################

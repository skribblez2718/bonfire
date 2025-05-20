import os

from bonfire.utils.file import BonfireFile
from bonfire.utils.result import BonfireResult


###################################[ start BonfireReport ]##############################################
class BonfireReport:
    """
    Class for generating reports from Bonfire analysis results.
    """

    #########################[ start generate_reports_for_analysis_file ]#########################
    @staticmethod
    def generate_reports_for_analysis_file(
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
        base, ext = os.path.splitext(os.path.basename(analysis_jsonl_path))

        #########################[ start post_process ]##############################################
        def post_process(intent_results, file_path, intent, logger):
            report_html_path = os.path.join(output_dir, f"{base}_report.html")
            BonfireFile.generate_html_report(intent_results, report_html_path, logger)
            logger.info(f"Generated report files: {file_path}, {report_html_path}")
            
        #########################[ end post_process ]################################################
        
        BonfireResult.save_by_intent(
            results,
            output_dir,
            filename_format=f"{base}_report{ext}",
            logger=logger,
            post_process=post_process
        )

    #########################[ end generate_reports_for_analysis_file ]#########################


#########################[ end BonfireReport ]################################################

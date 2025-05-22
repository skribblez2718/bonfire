import os
import sys
import glob

from dotenv import load_dotenv

from bonfire.utils import (
    BonfireLogger,
    BonfireCLI,
    BonfirePayloads,
    BonfireAnalyze,
    BonfireValidate,
    BonfireFile,
    BonfireReport,
    BonfireResult,
)


load_dotenv()


###################################[ start main ]###################################
def main() -> None:
    """
    Entrypoint for the Bonfire CLI.

    * Parses CLI arguments.
    * Loads instructions/templates.
    * Generates augmented payloads (text / audio / image).
    * Delegates all shared work to ``BonfireHelper`` utilities to avoid redundancy.
    """
    logger = BonfireLogger("bonfire")
    templates_dir = os.path.join(os.path.dirname(__file__), "data", "templates")
    available_methods = [
        os.path.splitext(f)[0]
        for f in os.listdir(templates_dir)
        if f.endswith(".jsonl")
    ]

    args = BonfireCLI.parse(available_methods)

    BonfireValidate.validate_env_vars(logger)

    payloads = BonfirePayloads.generate(
        logger,
        templates_dir,
        available_methods,
        args.methods,
        args.output_dir,
        args.data_type,
        args.format,
    )

    # Generate payloads and run test file if in test mode
    if args.command in ["test", "analyze", "report"]:
        import importlib.util
        import traceback

        test_file = args.test_file
        if not test_file.endswith(".py"):
            test_file_py = test_file + ".py"
        else:
            test_file_py = test_file
            test_file = test_file[:-3]

        functions_dir = os.path.join(os.path.dirname(__file__), "function")

        test_file_basename = os.path.basename(test_file_py)
        test_path = os.path.join(functions_dir, test_file_basename)

        if not os.path.isfile(test_path):
            logger.error(
                f"Test file '{test_file_basename}' not found in 'function' directory."
            )
            sys.exit(1)

        try:
            spec = importlib.util.spec_from_file_location(test_file, test_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            logger.error(
                f"Failed to import test module '{test_file_py}': {e}\n{traceback.format_exc()}"
            )
            sys.exit(1)

        if not hasattr(module, "run_test"):
            logger.error(
                f"No 'run_test' function found in '{test_file_py}'. Please define 'run_test(payloads)'."
            )
            sys.exit(1)

        try:
            logger.info(f"Running test '{test_file_py}'...")
            results = module.run_test(payloads)
            logger.info(f"Test '{test_file_py}' completed.")
        except Exception as e:
            logger.error(
                f"Error running 'run_test' in '{test_file_py}': {e}\n{traceback.format_exc()}"
            )
            sys.exit(1)

        # Write test results to output_dir, grouped by intent, as JSONL (one file per intent)
        BonfireResult.save_by_intent(
            results,
            args.output_dir,
            filename_format=f"bonfire_{args.data_type}_tests_{{intent}}.jsonl",
            logger=logger,
        )

    if args.command in ["analyze", "report"]:
        analysis_results = [
            BonfireAnalyze.send_request(result, logger) for result in results
        ]
        BonfireResult.save_by_intent(
            analysis_results,
            args.output_dir,
            filename_format=f"bonfire_{args.data_type}_analysis_{{intent}}.jsonl",
            logger=logger,
        )

    if args.command == "report":
        # Look for analysis files in output_dir/{intent} subdirectories
        pattern = os.path.join(args.output_dir, "*", "bonfire_*_analysis_*.jsonl")
        analysis_files = glob.glob(pattern)
        if not analysis_files:
            logger.warning(
                f"No analysis files found in any {args.output_dir}/{{intent}} matching 'bonfire_*_analysis_*.jsonl'."
            )

        for analysis_file in analysis_files:
            BonfireReport.generate(analysis_file, args.output_dir, logger)


###################################[ end main ]#####################################

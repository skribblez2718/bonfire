import argparse
import os
import sys

from dotenv import load_dotenv

from bonfire.utils import (
    BonfireLogger,
    BonfireCLI,
    BonfirePayloads,
)

load_dotenv()


###################################[ start main ]##############################################
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
    available_methods = [os.path.splitext(f)[0] for f in os.listdir(templates_dir) if f.endswith(".jsonl")]
    
    args = BonfireCLI.parse(available_methods)

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
    if args.command == "test":
        import importlib.util
        import traceback

        test_file = args.test_file
        if not test_file.endswith('.py'):
            test_file_py = test_file + '.py'
        else:
            test_file_py = test_file
            test_file = test_file[:-3]
        
        functions_dir = os.path.join(os.path.dirname(__file__), 'functions')
        test_path = os.path.join(functions_dir, test_file_py)
        
        if not os.path.isfile(test_path):
            logger.error(f"Test file '{test_file_py}' not found in 'functions' directory.")
            sys.exit(1)

        try:
            spec = importlib.util.spec_from_file_location(test_file, test_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            logger.error(f"Failed to import test module '{test_file_py}': {e}\n{traceback.format_exc()}")
            sys.exit(1)

        if not hasattr(module, 'run_test'):
            logger.error(f"No 'run_test' function found in '{test_file_py}'. Please define 'run_test(payloads)'.")
            sys.exit(1)

        try:
            logger.info(f"Running test '{test_file_py}'...")
            result = module.run_test(payloads)
            logger.info(f"Test '{test_file_py}' completed. Result: {result}")
        except Exception as e:
            logger.error(f"Error running 'run_test' in '{test_file_py}': {e}\n{traceback.format_exc()}")
            sys.exit(1)


###################################[ end main ]##############################################

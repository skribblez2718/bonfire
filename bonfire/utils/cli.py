from __future__ import annotations

import argparse
from typing import List


###################################[ start BonfireCLI ]###################################
class BonfireCLI:
    """
    Wrapper around :pymod:`argparse` that encapsulates all Bonfire-specific
    command-line options.
    """

    #########################[ start parse ]#########################
    @staticmethod
    def parse(available_methods: List[str]) -> argparse.Namespace:
        """
        Parse CLI arguments.

        Args:
            available_methods: List of detected augmentation methods.

        Returns:
            Parsed arguments as an :class:`argparse.Namespace`.
        """
        parser = BonfireCLI._build_parser(available_methods)
        return parser.parse_args()

    #########################[ end parse ]###########################

    #########################[ start _build_parser ]#################
    @staticmethod
    def _build_parser(available_methods: List[str]) -> argparse.ArgumentParser:
        """
        Construct the top-level parser and attach *generate* / *test* sub-parsers.

        Args:
            available_methods: Method names for the *--methods* help text.

        Returns:
            Configured :class:`argparse.ArgumentParser`.
        """
        parser = argparse.ArgumentParser(
            description="Bonfire: A tool for augmenting text, audio, and images"
        )
        subparsers = parser.add_subparsers(dest="command", required=True)

        # Attach sub-parsers
        BonfireCLI._build_generate_parser(subparsers, available_methods)
        BonfireCLI._build_test_parser(subparsers, available_methods)
        BonfireCLI._build_analyze_parser(subparsers, available_methods)
        BonfireCLI._build_report_parser(subparsers, available_methods)

        return parser

    #########################[ end _build_parser ]####################

    #########################[ start _add_shared_args ]################
    @staticmethod
    def _add_shared_args(parser, available_methods: List[str]):
        parser.add_argument(
            "data_type",
            choices=["text", "audio", "image"],
            help="Type of data to augment",
        )
        parser.add_argument(
            "format",
            nargs="?",
            default=None,
            help="Format for audio (wav/mp3) or image (jpeg/png/gif) data",
        )
        parser.add_argument(
            "methods",
            help=(
                "Augmentation method(s) to use. "
                "Single method, comma-separated list, or 'all'. "
                f"Available methods: {', '.join(available_methods)}"
            ),
        )
        parser.add_argument("output_dir", help="Directory path for saving data")

    #########################[ end _add_shared_args ]####################

    #########################[ start _build_generate_parser ]############
    @staticmethod
    def _build_generate_parser(
        subparsers: argparse._SubParsersAction, available_methods: List[str]
    ) -> argparse.ArgumentParser:
        """
        Create the *generate* sub-command parser.
        """
        gen = subparsers.add_parser("generate", help="Generate augmented data")
        BonfireCLI._add_shared_args(gen, available_methods)
        return gen

    #########################[ end _build_generate_parser ]##############

    #########################[ start _build_test_parser ]################
    @staticmethod
    def _build_test_parser(
        subparsers: argparse._SubParsersAction, available_methods: List[str]
    ) -> argparse.ArgumentParser:
        """
        Create the *test* sub-command parser.
        """
        test = subparsers.add_parser(
            "test",
            help="Runs generate and then tests the payloads against the LLM via defined Python script in function directory",
        )
        BonfireCLI._add_shared_args(test, available_methods)
        test.add_argument(
            "test_file",
            help="Name of the test file to run you created in the function directory",
        )
        return test

    #########################[ end _build_test_parser ]##################

    #########################[ start _build_analyze_parser ]#############
    @staticmethod
    def _build_analyze_parser(
        subparsers: argparse._SubParsersAction, available_methods: List[str]
    ) -> argparse.ArgumentParser:
        """
        Create the *analyze* sub-command parser (same options as test).
        """
        analyze = subparsers.add_parser(
            "analyze",
            help="Runs generate and then sends the results to a defined LLM for analysis",
        )
        BonfireCLI._add_shared_args(analyze, available_methods)
        analyze.add_argument(
            "test_file",
            help="Name of the test file to analyze you created in the function directory",
        )
        return analyze

    #########################[ end _build_analyze_parser ]###############

    #########################[ start _build_report_parser ]##############
    @staticmethod
    def _build_report_parser(
        subparsers: argparse._SubParsersAction, available_methods: List[str]
    ) -> argparse.ArgumentParser:
        """
        Create the *report* sub-command parser (same options as test).
        """
        report = subparsers.add_parser(
            "report",
            help="Runs generate, test and analyze then generates and HTML and JSONL report and save sthem to output_dir",
        )
        BonfireCLI._add_shared_args(report, available_methods)
        report.add_argument(
            "test_file",
            help="Name of the test file to report on you created in the function directory",
        )
        return report

    #########################[ end _build_report_parser ]################


###################################[ end BonfireCLI ]#####################################

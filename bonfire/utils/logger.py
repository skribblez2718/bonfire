import logging
import sys
from typing import Any

# ANSI color codes for terminal output
COLORS = {
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "BOLD": "\033[1m",
    "RESET": "\033[0m",
}


###################################[ start BonfireLogger ]##############################################
class BonfireLogger:
    """
    A logger class for the Bonfire application.
    """

    #########################[ start __init__ ]##############################################
    def __init__(self, name: str = "bonfire", level: int = logging.INFO) -> None:
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create console handler
        console_handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Create custom colored formatter
        class ColoredFormatter(logging.Formatter):
            def format(self, record):
                levelname = record.levelname
                message = super().format(record)

                if levelname == "INFO":
                    colored_levelname = f"{COLORS['BLUE']}{levelname}{COLORS['RESET']}"
                elif levelname == "WARNING":
                    colored_levelname = (
                        f"{COLORS['YELLOW']}{levelname}{COLORS['RESET']}"
                    )
                elif levelname in ("ERROR", "CRITICAL"):
                    colored_levelname = f"{COLORS['RED']}{levelname}{COLORS['RESET']}"
                else:
                    colored_levelname = levelname

                # Replace the original levelname with the colored version
                return message.replace(levelname, colored_levelname)

        # Create formatter with custom format
        formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(console_handler)

    #########################[ end __init__ ]################################################

    #########################[ start debug ]##############################################
    def debug(self, message: Any) -> None:
        self.logger.debug(message)

    #########################[ end debug ]################################################

    #########################[ start info ]##############################################
    def info(self, message: Any) -> None:
        self.logger.info(message)

    #########################[ end info ]################################################

    #########################[ start warning ]##############################################
    def warning(self, message: Any) -> None:
        self.logger.warning(message)

    #########################[ end warning ]################################################

    #########################[ start error ]##############################################
    def error(self, message: Any) -> None:
        self.logger.error(message)

    #########################[ end error ]################################################

    #########################[ start critical ]##############################################
    def critical(self, message: Any) -> None:
        self.logger.critical(message)

    #########################[ end critical ]################################################

    #########################[ start set_level ]##############################################
    def set_level(self, level: int) -> None:
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    #########################[ end set_level ]################################################


###################################[ end BonfireLogger ]##############################################

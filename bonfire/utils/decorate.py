import random
from typing import List


###################################[ start BonfireTextEvasionDecorate ]###################################
class BonfireTextEvasionDecorate:
    """
    Class for decorating text with various diacritics and stylistic elements.
    """

    _waves: List[str] = ["̾", "͂", "̽", "͌"]

    #########################[ start make_wavy_random ]#########################
    @staticmethod
    def make_wavy_random(text: str, probability: float = 0.15) -> str:
        """
        Add wave diacritics to random characters with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of adding a wave diacritic to each character (default: 0.15)

        Returns:
            str: Text with random characters made wavy
        """
        result = []
        for char in text:
            # Skip whitespace characters
            if char.isspace():
                result.append(char)
                continue

            # Add a wave diacritic to the character with the given probability
            if random.random() < probability:
                wave = random.choice(BonfireTextEvasionDecorate._waves)
                result.append(char + wave)
            else:
                result.append(char)

        return "".join(result)

    #########################[ end make_wavy_random ]###########################

    #########################[ start make_wavy_all ]############################
    @staticmethod
    def make_wavy_all(text: str) -> str:
        """
        Add wave diacritics to all characters (except whitespace).

        Args:
            text: Input text to modify

        Returns:
            str: Text with all non-whitespace characters made wavy
        """
        result = []
        for char in text:
            # Skip whitespace characters
            if char.isspace():
                result.append(char)
                continue

            # Add a random wave diacritic to each character
            wave = random.choice(BonfireTextEvasionDecorate._waves)
            result.append(char + wave)

        return "".join(result)

    #########################[ end make_wavy_all ]##############################

    #########################[ start make_strikethrough_random ]################
    @staticmethod
    def make_strikethrough_random(text: str, probability: float = 0.15) -> str:
        """
        Add strikethrough to random characters with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of adding a strikethrough to each character (default: 0.15)

        Returns:
            str: Text with random characters having strikethrough
        """
        result = []
        for char in text:
            # Skip whitespace characters
            if char.isspace():
                result.append(char)
                continue

            # Add a strikethrough to the character with the given probability
            if random.random() < probability:
                result.append(char + "̶")  # Combining long stroke overlay
            else:
                result.append(char)

        return "".join(result)

    #########################[ end make_strikethrough_random ]###################

    #########################[ start make_strikethrough_all ]####################
    @staticmethod
    def make_strikethrough_all(text: str) -> str:
        """
        Add strikethrough to all characters (except whitespace).

        Args:
            text: Input text to modify

        Returns:
            str: Text with all non-whitespace characters having strikethrough
        """
        result = []
        for char in text:
            # Skip whitespace characters
            if char.isspace():
                result.append(char)
                continue

            # Add a strikethrough to each character
            result.append(char + "̶")  # Combining long stroke overlay

        return "".join(result)

    #########################[ end make_strikethrough_all ]######################

    #########################[ start make_fullwidth_random ]#####################
    @staticmethod
    def make_fullwidth_random(text: str, probability: float = 0.15) -> str:
        """
        Convert random characters to fullwidth with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of converting each character to fullwidth (default: 0.15)

        Returns:
            str: Text with random characters converted to fullwidth
        """
        result = []
        for char in text:
            # Skip whitespace characters
            if char.isspace():
                result.append(char)
                continue

            # Convert the character to fullwidth with the given probability
            if random.random() < probability:
                # Convert to fullwidth (shift ASCII range)
                if 0x21 <= ord(char) <= 0x7E:
                    result.append(chr(ord(char) + 0xFEE0))
                else:
                    result.append(char)
            else:
                result.append(char)

        return "".join(result)

    #########################[ end make_fullwidth_random ]#######################

    #########################[ start make_fullwidth_all ]########################
    @staticmethod
    def make_fullwidth_all(text: str) -> str:
        """
        Convert all characters to fullwidth (except whitespace).

        Args:
            text: Input text to modify

        Returns:
            str: Text with all non-whitespace characters converted to fullwidth
        """
        result = []
        for char in text:
            # Skip whitespace characters
            if char.isspace():
                result.append(char)
                continue

            # Convert the character to fullwidth
            # Convert to fullwidth (shift ASCII range)
            if 0x21 <= ord(char) <= 0x7E:
                result.append(chr(ord(char) + 0xFEE0))
            else:
                result.append(char)

        return "".join(result)

    #########################[ end make_fullwidth_all ]##########################

    #########################[ start make_wide_space_random ]####################
    @staticmethod
    def make_wide_space_random(text: str, probability: float = 0.15) -> str:
        """
        Add spaces between random characters with a given probability (vaporwave aesthetic).

        Args:
            text: Input text to modify
            probability: Probability of adding spaces between characters (default: 0.15)

        Returns:
            str: Text with spaces added between random characters
        """
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            # Skip existing whitespace characters
            if char.isspace():
                result.append(char)
                i += 1
                continue

            # Add the character
            result.append(char)

            # Add a space after the character with the given probability
            # Only if the next character isn't whitespace and we're not at the end
            if (
                random.random() < probability
                and i < len(text) - 1
                and not text[i + 1].isspace()
            ):
                result.append(" ")

            i += 1

        return "".join(result)

    #########################[ end make_wide_space_random ]######################

    #########################[ start make_wide_space_all ]#######################
    @staticmethod
    def make_wide_space_all(text: str) -> str:
        """
        Add spaces between all characters (vaporwave aesthetic).

        Args:
            text: Input text to modify

        Returns:
            str: Text with spaces added between all characters
        """
        result = []

        # Process each character
        for i, char in enumerate(text):
            # Skip existing whitespace characters
            if char.isspace():
                result.append(char)
                continue

            # Add the character
            result.append(char)

            # Add a space after the character if it's not the last character
            # and the next character isn't whitespace
            if i < len(text) - 1 and not text[i + 1].isspace():
                result.append(" ")

        return "".join(result)

    #########################[ end make_wide_space_all ]#########################


###################################[ end BonfireTextEvasionDecorate ]#####################################

import random
from typing import List


###################################[ start BonfireTextEvasionWhitespace ]##############################################
class BonfireTextEvasionWhitespace:
    """
    Class for whitespace-based text evasion techniques.
    Contains methods for adding random spaces, zero-width spaces, and newlines.
    Both random (probability-based) and all (applied to all eligible characters) versions are provided.
    """

    #########################[ start add_spaces_random ]##############################################
    @staticmethod
    def add_spaces_random(text: str, probability: float = 0.15) -> str:
        """
        Randomly add spaces between characters with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of adding a space after each character (default: 0.15)

        Returns:
            str: Text with random spaces added
        """
        result = []
        for char in text:
            result.append(char)
            # Add a space after the character with the given probability
            # Don't add spaces after spaces to avoid consecutive spaces
            if char != " " and random.random() < probability:
                result.append(" ")

        return "".join(result)

    #########################[ end add_spaces_random ]################################################

    #########################[ start add_spaces_all ]##############################################
    @staticmethod
    def add_spaces_all(text: str) -> str:
        """
        Add spaces between all characters (except after existing spaces).

        Args:
            text: Input text to modify

        Returns:
            str: Text with spaces added between all characters
        """
        result = []
        for char in text:
            result.append(char)
            # Add a space after each character except spaces
            if char != " ":
                result.append(" ")

        return "".join(result)

    #########################[ end add_spaces_all ]################################################

    #########################[ start add_zero_width_spaces_random ]##############################################
    @staticmethod
    def add_zero_width_spaces_random(text: str, probability: float = 0.25) -> str:
        """
        Randomly add zero-width spaces (U+200B) between characters with a given probability.
        These spaces are invisible but can disrupt text analysis systems.

        Args:
            text: Input text to modify
            probability: Probability of adding a zero-width space after each character (default: 0.25)

        Returns:
            str: Text with zero-width spaces added
        """
        zero_width_space = "\u200b"  # Unicode zero-width space
        result = []
        for char in text:
            result.append(char)
            # Add a zero-width space after the character with the given probability
            if random.random() < probability:
                result.append(zero_width_space)

        return "".join(result)

    #########################[ end add_zero_width_spaces_random ]################################################

    #########################[ start add_zero_width_spaces_all ]##############################################
    @staticmethod
    def add_zero_width_spaces_all(text: str) -> str:
        """
        Add zero-width spaces (U+200B) between all characters.
        These spaces are invisible but can disrupt text analysis systems.

        Args:
            text: Input text to modify

        Returns:
            str: Text with zero-width spaces added between all characters
        """
        zero_width_space = "\u200b"  # Unicode zero-width space
        result = []
        for char in text:
            result.append(char)
            # Add a zero-width space after every character
            result.append(zero_width_space)

        return "".join(result)

    #########################[ end add_zero_width_spaces_all ]################################################

    #########################[ start newline_random ]##############################################
    @staticmethod
    def newline_random(text: str, probability: float = 0.2) -> str:
        """
        Randomly add newlines inside and between words.

        Args:
            text: The text to augment
            probability: Probability of adding a newline after each character (default: 0.2)

        Returns:
            str: The augmented text with random newlines added
        """
        result = []
        words = text.split()

        # Process each word
        for i, word in enumerate(words):
            # Randomly add newlines between words
            if i > 0 and random.random() < probability:
                result.append("\n")

            # Process characters within the word
            word_chars = []
            for char in word:
                word_chars.append(char)
                # Randomly add newlines within words
                if (
                    random.random() < probability / 2
                ):  # Lower probability for within words
                    word_chars.append("\n")

            result.append("".join(word_chars))

        return " ".join(result)

    #########################[ end newline_random ]################################################

    #########################[ start newline_all ]##############################################
    @staticmethod
    def newline_all(text: str) -> str:
        """
        Add newlines after every character and between all words.

        Args:
            text: The text to augment

        Returns:
            str: The augmented text with newlines added after every character
        """
        result = []
        words = text.split()

        # Process each word
        for i, word in enumerate(words):
            # Add newlines between all words
            if i > 0:
                result.append("\n")

            # Process characters within the word
            word_chars = []
            for char in word:
                word_chars.append(char)
                # Add newlines after every character
                word_chars.append("\n")

            result.append("".join(word_chars))

        return " ".join(result)

    #########################[ end newline_all ]################################################


###################################[ end BonfireTextEvasionWhitespace ]##############################################

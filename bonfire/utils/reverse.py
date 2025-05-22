import random
from typing import Dict


###################################[ start BonfireTextEvasionReverse ]###################################
class BonfireTextEvasionReverse:
    """
    Class for text reversal evasion techniques.
    Contains methods for sentence reversal and word reversal.
    """

    #########################[ start sentence_reverse_all ]#########################
    @staticmethod
    def sentence_reverse_all(text: str) -> str:
        """
        Reverse the word order of the sentence.

        Args:
            text: The text to augment

        Returns:
            str: The text with words in reverse order
        """
        words = text.split()
        reversed_words = words[::-1]  # Reverse the list of words
        return " ".join(reversed_words)

    #########################[ end sentence_reverse_all ]###########################

    #########################[ start sentence_reverse_random ]######################
    @staticmethod
    def sentence_reverse_random(text: str, probability: float = 0.7) -> str:
        """
        Put all words in the sentence in a random order with a given probability.

        Args:
            text: The text to augment
            probability: Probability of shuffling the sentence (default: 0.7)

        Returns:
            str: The text with words in random order
        """
        sentences = text.split(".")
        result = []

        for sentence in sentences:
            if not sentence.strip():
                result.append(sentence)
                continue

            if random.random() < probability:
                words = sentence.split()
                random.shuffle(words)  # Randomly shuffle the words
                result.append(" ".join(words))
            else:
                result.append(sentence)

        return ".".join(result)

    #########################[ end sentence_reverse_random ]#########################

    #########################[ start word_reverse_random ]###########################
    @staticmethod
    def word_reverse_random(text: str, probability: float = 0.5) -> str:
        """
        Reverse the letters of individual words in the text with a given probability.

        Args:
            text: The text to augment
            probability: Probability of reversing each word (default: 0.5)

        Returns:
            str: The text with some words reversed
        """
        words = text.split()
        result = []

        for word in words:
            if random.random() < probability:
                # Reverse the characters in the word
                reversed_word = word[::-1]
                result.append(reversed_word)
            else:
                result.append(word)

        return " ".join(result)

    #########################[ end word_reverse_random ]#############################

    #########################[ start word_reverse_all ]##############################
    @staticmethod
    def word_reverse_all(text: str) -> str:
        """
        Reverse the letters of all words in the text.

        Args:
            text: The text to augment

        Returns:
            str: The text with all words reversed
        """
        words = text.split()
        result = []

        for word in words:
            # Reverse the characters in the word
            reversed_word = word[::-1]
            result.append(reversed_word)

        return " ".join(result)

    #########################[ end word_reverse_all ]################################

    _upside_down_chars: Dict[str, str] = {
        "a": "ɐ",
        "b": "q",
        "c": "ɔ",
        "d": "p",
        "e": "ǝ",
        "f": "ɟ",
        "g": "ƃ",
        "h": "ɥ",
        "i": "ɨ",
        "j": "ɾ",
        "k": "ʞ",
        "l": "l",
        "m": "ɯ",
        "n": "u",
        "o": "ɔ",
        "p": "d",
        "q": "b",
        "r": "ɹ",
        "s": "s",
        "t": "ʇ",
        "u": "n",
        "v": "ʌ",
        "w": "ʍ",
        "x": "x",
        "y": "ʎ",
        "z": "z",
    }

    # Upside down character mapping
    _upside_down_chars: Dict[str, str] = {
        "a": "ɐ",
        "b": "q",
        "c": "ɔ",
        "d": "p",
        "e": "ǝ",
        "f": "ɟ",
        "g": "ƃ",
        "h": "ɥ",
        "i": "ı",
        "j": "ɾ",
        "k": "ʞ",
        "l": "l",
        "m": "ɯ",
        "n": "u",
        "o": "o",
        "p": "d",
        "q": "b",
        "r": "ɹ",
        "s": "s",
        "t": "ʇ",
        "u": "n",
        "v": "ʌ",
        "w": "ʍ",
        "x": "x",
        "y": "ʎ",
        "z": "z",
        "A": "Ɐ",
        "B": "B",
        "C": "Ɔ",
        "D": "D",
        "E": "Ǝ",
        "F": "Ⅎ",
        "G": "פ",
        "H": "H",
        "I": "I",
        "J": "ſ",
        "K": "ʞ",
        "L": "˥",
        "M": "W",
        "N": "N",
        "O": "O",
        "P": "Ԁ",
        "Q": "Q",
        "R": "ꓤ",
        "S": "S",
        "T": "┴",
        "U": "∩",
        "V": "Λ",
        "W": "M",
        "X": "X",
        "Y": "⅄",
        "Z": "Z",
        "0": "0",
        "1": "Ɩ",
        "2": "ᄅ",
        "3": "Ɛ",
        "4": "ㄣ",
        "5": "ϛ",
        "6": "9",
        "7": "ㄥ",
        "8": "8",
        "9": "6",
        ".": "˙",
        ",": "'",
        "?": "¿",
        "!": "¡",
        '"': ",,",
        "'": ",",
        "(": ")",
        ")": "(",
        "[": "]",
        "]": "[",
        "{": "}",
        "}": "{",
        "<": ">",
        ">": "<",
        "&": "⅋",
        "_": "‾",
    }

    #########################[ start _convert_to_upside_dow]#########################
    @staticmethod
    def _convert_to_upside_down(text: str) -> str:
        """
        Convert text to upside down characters using the mapping.

        Args:
            text: The text to convert

        Returns:
            str: The upside down text
        """
        upside_down_text = ""
        for char in text:
            upside_down_text += BonfireTextEvasionReverse._upside_down_chars.get(
                char, char
            )
        return upside_down_text

    #########################[ end _convert_to_upside_down ]#########################

    #########################[ start word_upside_down_random ]#######################
    @staticmethod
    def word_upside_down_random(text: str, probability: float = 0.5) -> str:
        """
        Convert all characters of randomly selected words to upside down with a given probability.

        Args:
            text: The text to augment
            probability: Probability of converting each word (default: 0.5)

        Returns:
            str: The text with some words converted to upside down
        """
        words = text.split()
        result = []

        for word in words:
            if random.random() < probability:
                # Convert the word to upside down characters
                upside_down_word = BonfireTextEvasionReverse._convert_to_upside_down(
                    word
                )
                result.append(upside_down_word)
            else:
                result.append(word)

        return " ".join(result)

    #########################[ end word_upside_down_random ]#########################

    #########################[ start word_upside_down_all ]##########################
    @staticmethod
    def word_upside_down_all(text: str) -> str:
        """
        Convert all characters of all words to upside down.

        Args:
            text: The text to augment

        Returns:
            str: The text with all words converted to upside down
        """
        words = text.split()
        result = []

        for word in words:
            # Convert the word to upside down characters
            upside_down_word = BonfireTextEvasionReverse._convert_to_upside_down(word)
            result.append(upside_down_word)

        return " ".join(result)

    #########################[ end word_upside_down_all ]#############################

    #########################[ start char_upside_down_random ]########################
    @staticmethod
    def char_upside_down_random(text: str, probability: float = 0.3) -> str:
        """
        Convert random characters to upside down with a given probability.

        Args:
            text: The text to augment
            probability: Probability of converting each character (default: 0.3)

        Returns:
            str: The text with random characters converted to upside down
        """
        result = ""

        for char in text:
            if random.random() < probability:
                # Convert the character to upside down
                upside_down_char = BonfireTextEvasionReverse._upside_down_chars.get(
                    char, char
                )
                result += upside_down_char
            else:
                result += char

        return result

    #########################[ end char_upside_down_random ]##########################

    _mirrored_chars: Dict[str, str] = {
        "a": "ɒ",
        "b": "d",
        "c": "ɔ",
        "d": "b",
        "e": "ɘ",
        "f": "Ꮈ",
        "g": "ǫ",
        "h": "ʜ",
        "i": "i",
        "j": "į",
        "k": "ʞ",
        "l": "|",
        "m": "m",
        "n": "ᴎ",
        "o": "o",
        "p": "q",
        "q": "p",
        "r": "ɿ",
        "s": "ƨ",
        "t": "ƚ",
        "u": "u",
        "v": "v",
        "w": "w",
        "x": "x",
        "y": "y",
        "z": "z",
        " ": " ",
    }

    #########################[ start _convert_to_mirrored ]###########################
    @staticmethod
    def _convert_to_mirrored(text: str) -> str:
        """
        Convert text to mirrored characters using the mapping.

        Args:
            text: The text to convert

        Returns:
            str: The mirrored text
        """
        mirrored_text = ""
        for char in text:
            mirrored_text += BonfireTextEvasionReverse._mirrored_chars.get(char, char)
        return mirrored_text

    #########################[ end _convert_to_mirrored ]#############################

    #########################[ start word_mirrored_random ]###########################
    @staticmethod
    def word_mirrored_random(text: str, probability: float = 0.5) -> str:
        """
        Convert all characters of randomly selected words to mirrored with a given probability.

        Args:
            text: The text to augment
            probability: Probability of converting each word (default: 0.5)

        Returns:
            str: The text with some words converted to mirrored characters
        """
        words = text.split()
        result = []

        for word in words:
            if random.random() < probability:
                # Convert the word to mirrored characters
                mirrored_word = BonfireTextEvasionReverse._convert_to_mirrored(word)
                result.append(mirrored_word)
            else:
                result.append(word)

        return " ".join(result)

    #########################[ end word_mirrored_random ]#############################

    #########################[ start word_mirrored_all ]##############################
    @staticmethod
    def word_mirrored_all(text: str) -> str:
        """
        Convert all characters of all words to mirrored.

        Args:
            text: The text to augment

        Returns:
            str: The text with all words converted to mirrored characters
        """
        words = text.split()
        result = []

        for word in words:
            # Convert the word to mirrored characters
            mirrored_word = BonfireTextEvasionReverse._convert_to_mirrored(word)
            result.append(mirrored_word)

        return " ".join(result)

    #########################[ end word_mirrored_all ]################################

    #########################[ start char_mirrored_random ]###########################
    @staticmethod
    def char_mirrored_random(text: str, probability: float = 0.3) -> str:
        """
        Convert random characters to mirrored with a given probability.

        Args:
            text: The text to augment
            probability: Probability of converting each character (default: 0.3)

        Returns:
            str: The text with random characters converted to mirrored
        """
        result = ""

        for char in text:
            if random.random() < probability:
                # Convert the character to mirrored
                mirrored_char = BonfireTextEvasionReverse._mirrored_chars.get(
                    char, char
                )
                result += mirrored_char
            else:
                result += char

        return result

    #########################[ end char_mirrored_random ]#############################

    #########################[ start char_mirrored_all ]##############################
    @staticmethod
    def char_mirrored_all(text: str) -> str:
        """
        Convert all characters to mirrored.

        Args:
            text: The text to augment

        Returns:
            str: The text with all characters converted to mirrored
        """
        result = ""

        for char in text:
            # Convert the character to mirrored
            mirrored_char = BonfireTextEvasionReverse._mirrored_chars.get(char, char)
            result += mirrored_char

        return result

    #########################[ end char_mirrored_all ]################################


###################################[ end BonfireTextEvasionReverse ]#####################################

import random
from typing import Dict, List


###################################[ start BonfireTextEvasionLanguage ]###################################
class BonfireTextEvasionLanguage:
    """
    Class for language-based text evasion techniques.
    Contains methods for adding diacritics and converting text to l33t speak.
    """

    # Comprehensive mapping of letters to their diacritic variants
    _diacritic_map = {
        "a": ["à", "á", "â", "ä", "å", "ã", "ă", "ą"],
        "c": ["ç", "ć", "č"],
        "d": ["ď", "đ"],
        "e": ["è", "é", "ê", "ë", "ě", "ę"],
        "g": ["ğ"],
        "i": ["ì", "í", "î", "ï"],
        "l": ["ł", "ľ"],
        "n": ["ñ", "ń", "ň"],
        "o": ["ò", "ó", "ô", "ö", "õ", "ø", "ő"],
        "r": ["ř"],
        "s": ["ś", "š"],
        "t": ["ť"],
        "u": ["ù", "ú", "û", "ü", "ů", "ű"],
        "y": ["ý", "ÿ"],
        "z": ["ź", "ž", "ż"],
        # Uppercase versions
        "A": ["À", "Á", "Â", "Ä", "Å", "Ã", "Ă", "Ą"],
        "C": ["Ç", "Ć", "Č"],
        "D": ["Ď", "Đ"],
        "E": ["È", "É", "Ê", "Ë", "Ě", "Ę"],
        "G": ["Ğ"],
        "I": ["Ì", "Í", "Î", "Ï"],
        "L": ["Ł", "Ľ"],
        "N": ["Ñ", "Ń", "Ň"],
        "O": ["Ò", "Ó", "Ô", "Ö", "Õ", "Ø", "Ő"],
        "R": ["Ř"],
        "S": ["Ś", "Š"],
        "T": ["Ť"],
        "U": ["Ù", "Ú", "Û", "Ü", "Ů", "Ű"],
        "Y": ["Ý", "Ÿ"],
        "Z": ["Ź", "Ž", "Ż"],
    }

    #########################[ start add_diacritics_random ]#########################
    @staticmethod
    def add_diacritics_random(text: str, probability: float = 0.3) -> str:
        """
        Add diacritics to letters in the text with a given probability.
        Includes diacritics from French, Spanish, German, Scandinavian, and Slovak languages.

        Args:
            text: Input text to modify
            probability: Probability of adding a diacritic to each letter (default: 0.3)

        Returns:
            str: Text with diacritics added
        """
        result = []
        for char in text:
            if (
                char in BonfireTextEvasionLanguage._diacritic_map
                and random.random() < probability
            ):
                # Replace with a random diacritic variant
                result.append(
                    random.choice(BonfireTextEvasionLanguage._diacritic_map[char])
                )
            else:
                result.append(char)

        return "".join(result)

    #########################[ end add_diacritics_random ]###########################

    #########################[ start add_diacritics_all ]############################
    @staticmethod
    def add_diacritics_all(text: str) -> str:
        """
        Add diacritics to all eligible letters in the text.
        Includes diacritics from French, Spanish, German, Scandinavian, and Slovak languages.

        Args:
            text: Input text to modify

        Returns:
            str: Text with diacritics added to all eligible characters
        """
        result = []
        for char in text:
            if char in BonfireTextEvasionLanguage._diacritic_map:
                # Replace with a random diacritic variant
                result.append(
                    random.choice(BonfireTextEvasionLanguage._diacritic_map[char])
                )
            else:
                result.append(char)

        return "".join(result)

    #########################[ end add_diacritics_all ]##############################

    # Define l33t speak mapping
    _l33t_map: Dict[str, List[str]] = {
        "a": ["4", "@", "/-\\", "^"],
        "b": ["8", "|3", "13", "|8"],
        "c": ["(", "<", "[", "©"],
        "d": ["|)", "o|", "[)", "|>"],
        "e": ["3", "€", "&", "[-"],
        "f": ["|=", "ph", "|#", "/="],
        "g": ["6", "9", "&", "C-"],
        "h": ["#", "|-|", "]-[", "(-)", ":-:"],
        "i": ["1", "!", "|", "eye"],
        "j": ["_|", "¿", "_/", "_7"],
        "k": ["|<", "|{", "|(", "|X"],
        "l": ["1", "|", "|_", "£"],
        "m": ["|\\/|", "/\\/\\", "|v|", "/v\\"],
        "n": ["|\\|", "/\\/", "|\\\\|", "/v"],
        "o": ["0", "()", "[]", "{}"],
        "p": ["|°", "|>", "|*", "|D"],
        "q": ["0_", "0,", "(,)", "kw"],
        "r": ["|2", "|?", "/2", "|^"],
        "s": ["5", "$", "z", "§"],
        "t": ["7", "+", "†", "|\\"],
        "u": ["|_|", "\\_\\", "\\_/", "(_)"],
        "v": ["\\/", "|/", "\\|", "\\/"],
        "w": ["\\/\\/", "vv", "\\^/", "\\|/"],
        "x": ["><", ")(", "}{", "×"],
        "y": ["`/", "¥", "\\|/", "`("],
        "z": ["2", "7_", "%", ">_"],
    }

    #########################[ start convert_to_l33t_random ]########################
    @staticmethod
    def convert_to_l33t_random(text: str, probability: float = 0.7) -> str:
        """
        Convert text to l33t speak by replacing letters with numbers and symbols.
        Only applies the conversion to some words based on probability.

        Args:
            text: Input text to modify
            probability: Probability of converting each word (default: 0.7)

        Returns:
            str: Text converted to l33t speak
        """
        # Process text word by word
        words = text.split()
        result = []

        for word in words:
            # Decide whether to convert this word
            if random.random() < probability:
                l33t_word = []
                for char in word:
                    lower_char = char.lower()
                    if lower_char in BonfireTextEvasionLanguage._l33t_map:
                        # Choose a random l33t replacement
                        replacement = random.choice(
                            BonfireTextEvasionLanguage._l33t_map[lower_char]
                        )
                        l33t_word.append(replacement)
                    else:
                        l33t_word.append(char)
                result.append("".join(l33t_word))
            else:
                result.append(word)

        return " ".join(result)

    #########################[ end convert_to_l33t_random ]##########################

    #########################[ start convert_to_l33t_all ]##########################
    @staticmethod
    def convert_to_l33t_all(text: str) -> str:
        """
        Convert all eligible characters in text to  l33t speak by replacing letters with numbers and symbols.

        Args:
            text: Input text to modify

        Returns:
            str: Text with all eligible characters converted to l33t speak
        """
        result = []
        for char in text:
            lower_char = char.lower()
            if lower_char in BonfireTextEvasionLanguage._l33t_map:
                # Choose a random l33t replacement
                replacement = random.choice(
                    BonfireTextEvasionLanguage._l33t_map[lower_char]
                )
                result.append(replacement)
            else:
                result.append(char)

        return "".join(result)

    #########################[ end convert_to_l33t_all ]############################

    _futhark_char: Dict[str, str] = {
        "a": "ᚨ",
        "b": "ᛒ",
        "c": "ᛲ",
        "d": "ᛞ",
        "e": "ᛖ",
        "f": "ᚠ",
        "g": "ᚷ",
        "h": "ᚺ",
        "i": "ᛁ",
        "j": "ᛃ",
        "k": "ᛲ",
        "l": "ᛚ",
        "m": "ᛗ",
        "n": "ᚾ",
        "o": "ᛟ",
        "p": "ᛈ",
        "q": "ᛲᛩ",
        "r": "ᚱ",
        "s": "ᛋ",
        "t": "ᛏ",
        "u": "ᚢ",
        "v": "ᛩ",
        "w": "ᛩ",
        "x": "ᛲᛋ",
        "y": "ᛁ",
        "z": "ᛉ",
        "A": "ᚨ",
        "B": "ᛒ",
        "C": "ᛲ",
        "D": "ᛞ",
        "E": "ᛖ",
        "F": "ᚠ",
        "G": "ᚷ",
        "H": "ᚺ",
        "I": "ᛁ",
        "J": "ᛃ",
        "K": "ᛲ",
        "L": "ᛚ",
        "M": "ᛗ",
        "N": "ᚾ",
        "O": "ᛟ",
        "P": "ᛈ",
        "Q": "ᛲᛩ",
        "R": "ᚱ",
        "S": "ᛋ",
        "T": "ᛏ",
        "U": "ᚢ",
        "V": "ᛩ",
        "W": "ᛩ",
        "X": "ᛲᛋ",
        "Y": "ᛁ",
        "Z": "ᛉ",
        " ": " ",
    }

    #########################[ start convert_to_futhark_random ]####################
    @staticmethod
    def convert_to_futhark_random(text: str, probability: float = 0.7) -> str:
        """
        Convert text to futhark runes by replacing letters with runic symbols.
        Only applies the conversion to some words based on probability.

        Args:
            text: Input text to modify
            probability: Probability of converting each word (default: 0.7)

        Returns:
            str: Text converted to futhark runes
        """
        # Process text word by word
        words = text.split()
        result = []

        for word in words:
            # Decide whether to convert this word
            if random.random() < probability:
                futhark_word = []
                for char in word:
                    if char in BonfireTextEvasionLanguage._futhark_char:
                        # Get the futhark rune replacement
                        replacement = BonfireTextEvasionLanguage._futhark_char[char]
                        futhark_word.append(replacement)
                    else:
                        futhark_word.append(char)
                result.append("".join(futhark_word))
            else:
                result.append(word)

        return " ".join(result)

    #########################[ end convert_to_futhark_random ]######################

    #########################[ start convert_to_futhark_all ]#######################
    @staticmethod
    def convert_to_futhark_all(text: str) -> str:
        """
        Convert all eligible characters in text to futhark runes by replacing letters with runic symbols.

        Args:
            text: Input text to modify

        Returns:
            str: Text with all eligible characters converted to futhark runes
        """
        result = []
        for char in text:
            if char in BonfireTextEvasionLanguage._futhark_char:
                # Get the futhark rune replacement
                replacement = BonfireTextEvasionLanguage._futhark_char[char]
                result.append(replacement)
            else:
                result.append(char)

        return "".join(result)

    #########################[ end convert_to_futhark_all ]#########################

    _medieval_chars: Dict[str, str] = {
        "a": "𝔞",
        "b": "𝔟",
        "c": "𝔠",
        "d": "𝔡",
        "e": "𝔢",
        "f": "𝔣",
        "g": "𝔤",
        "h": "𝔥",
        "i": "𝔦",
        "j": "𝔧",
        "k": "𝔨",
        "l": "𝔩",
        "m": "𝔪",
        "n": "𝔫",
        "o": "𝔬",
        "p": "𝔭",
        "q": "𝔮",
        "r": "𝔯",
        "s": "𝔰",
        "t": "𝔱",
        "u": "𝔲",
        "v": "𝔳",
        "w": "𝔴",
        "x": "𝔵",
        "y": "𝔶",
        "z": "𝔷",
        "A": "𝔄",
        "B": "𝔅",
        "C": "ℭ",
        "D": "𝔇",
        "E": "𝔈",
        "F": "𝔉",
        "G": "𝔊",
        "H": "ℌ",
        "I": "ℑ",
        "J": "𝔍",
        "K": "𝔎",
        "L": "𝔏",
        "M": "𝔐",
        "N": "𝔑",
        "O": "𝔒",
        "P": "𝔓",
        "Q": "𝔔",
        "R": "ℜ",
        "S": "𝔖",
        "T": "𝔗",
        "U": "𝔘",
        "V": "𝔙",
        "W": "𝔚",
        "X": "𝔛",
        "Y": "𝔜",
        "Z": "ℨ",
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        " ": " ",
    }

    #########################[ start convert_to_medieval_random ]###################
    @staticmethod
    def convert_to_medieval_random(text: str, probability: float = 0.5) -> str:
        """
        Convert random characters to their medieval Unicode equivalents with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of converting each character (default: 0.5)

        Returns:
            str: Text with random characters converted to medieval Unicode characters
        """
        result = []
        for char in text:
            if (
                random.random() < probability
                and char in BonfireTextEvasionLanguage._medieval_chars
            ):
                # Replace with medieval character
                result.append(BonfireTextEvasionLanguage._medieval_chars[char])
            else:
                result.append(char)

        return "".join(result)

    #########################[ end convert_to_medieval_random ]#####################

    #########################[ start convert_to_medieval_all ]######################
    @staticmethod
    def convert_to_medieval_all(text: str) -> str:
        """
        Convert all eligible characters to their medieval Unicode equivalents.

        Args:
            text: Input text to modify

        Returns:
            str: Text with all eligible characters converted to medieval Unicode characters
        """
        result = []
        for char in text:
            if char in BonfireTextEvasionLanguage._medieval_chars:
                # Replace with medieval character
                result.append(BonfireTextEvasionLanguage._medieval_chars[char])
            else:
                result.append(char)

        return "".join(result)

    #########################[ end convert_to_medieval_all ]########################

    _morse_code: Dict[str, str] = {
        "a": ".-",
        "b": "-...",
        "c": "-.-.",
        "d": "-..",
        "e": ".",
        "f": "..-.",
        "g": "--.",
        "h": "....",
        "i": "..",
        "j": ".---",
        "k": "-.-",
        "l": ".-..",
        "m": "--",
        "n": "-.",
        "o": "---",
        "p": ".--.",
        "q": "--.-",
        "r": ".-.",
        "s": "...",
        "t": "-",
        "u": "..-",
        "v": "...-",
        "w": ".--",
        "x": "-..-",
        "y": "-.--",
        "z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        " ": " ",
    }

    #########################[ start convert_morse_random ]#########################
    @staticmethod
    def convert_morse_random(text: str, probability: float = 0.5) -> str:
        """
        Convert random characters to their Morse code equivalents with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of converting each character (default: 0.5)

        Returns:
            str: Text with random characters converted to Morse code
        """
        result = []
        for char in text.lower():
            if (
                random.random() < probability
                and char in BonfireTextEvasionLanguage._morse_code
            ):
                # Replace with Morse code
                result.append(BonfireTextEvasionLanguage._morse_code[char])
            else:
                result.append(char)

        return "".join(result)

    #########################[ end convert_morse_random ]###########################

    #########################[ start convert_morse_all ]############################
    @staticmethod
    def convert_morse_all(text: str) -> str:
        """
        Convert all eligible characters to their Morse code equivalents.

        Args:
            text: Input text to modify

        Returns:
            str: Text with all eligible characters converted to Morse code
        """
        result = []
        for char in text.lower():
            if char in BonfireTextEvasionLanguage._morse_code:
                # Replace with Morse code
                result.append(BonfireTextEvasionLanguage._morse_code[char])
            else:
                result.append(char)

        return "".join(result)

    #########################[ end convert_morse_all ]##############################


###################################[ end BonfireTextEvasionLanguage ]#####################################

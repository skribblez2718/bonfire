import random
import base64
import re
from typing import List, Dict


###################################[ start BonfireTextEvasionEncode ]##############################################
class BonfireTextEvasionEncode:
    """
    Class for encoding-based text evasion techniques.
    Contains methods for adding similar Unicode characters, math symbols, Base64 encoding,
    hex encoding, HTML entities, and emoji variation selectors.
    """

    # Dictionary of similar Unicode characters for various letters
    _similar_unicode_chars: Dict[str, List[str]] = {
        "a": ["а", "ɑ", "α", "ạ", "ả", "ấ", "ầ", "ẩ", "ẫ", "ậ"],
        "b": ["ƀ", "Ɓ", "Ƃ", "ƃ", "ɓ"],
        "c": ["ⅽ", "ⅾ", "ⅿ", "ↄ"],
        "d": ["ⅾ", "Ⅿ", "ⅾ", "ⅾ"],
        "e": ["е", "е", "е", "е", "е"],
        "f": ["ƒ", "Ƒ"],
        "g": ["ɡ", "ɢ", "ɣ", "ɤ"],
        "h": ["һ", "Һ", "ḥ", "ḧ", "ḩ", "ḫ"],
        "i": ["і", "і", "і", "і", "і"],
        "j": ["ј", "ј", "ј", "ј"],
        "k": ["к", "к", "к", "к"],
        "l": ["ⅼ", "ⅽ", "ⅾ", "ⅿ"],
        "m": ["ⅿ", "ⅾ", "ⅿ", "ⅿ"],
        "n": ["п", "п", "п", "п"],
        "o": ["о", "о", "о", "о"],
        "p": ["р", "р", "р", "р"],
        "q": ["գ", "դ", "ե"],
        "r": ["г", "г", "г", "г"],
        "s": ["ѕ", "ѕ", "ѕ", "ѕ"],
        "t": ["т", "т", "т", "т"],
        "u": ["ս", "ս", "ս", "ս"],
        "v": ["ѵ", "ѵ", "ѵ", "ѵ"],
        "w": ["ա", "ա", "ա", "ա"],
        "x": ["х", "х", "х", "х"],
        "y": ["у", "у", "у", "у"],
        "z": ["ѕ", "ѕ", "ѕ", "ѕ"],
    }

    #########################[ start similar_unicode_chars_random ]##############################################
    @staticmethod
    def similar_unicode_chars_random(text: str, probability: float = 0.3) -> str:
        """
        Add similar Unicode characters to the text with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of adding a similar Unicode character after each character (default: 0.3)

        Returns:
            str: Text with similar Unicode characters added
        """
        result = []
        for char in text:
            result.append(char)
            if (
                char.lower() in BonfireTextEvasionEncode._similar_unicode_chars
                and random.random() < probability
            ):
                similar_chars = BonfireTextEvasionEncode._similar_unicode_chars[
                    char.lower()
                ]
                result.append(random.choice(similar_chars))

        return "".join(result)

    #########################[ end similar_unicode_chars_random ]################################################

    #########################[ start similar_unicode_chars_all ]##############################################
    @staticmethod
    def similar_unicode_chars_all(text: str) -> str:
        """
        Add similar Unicode characters to all eligible characters in the text.

        Args:
            text: Input text to modify

        Returns:
            str: Text with similar Unicode characters added to all eligible characters
        """
        result = []
        for char in text:
            result.append(char)
            if char.lower() in BonfireTextEvasionEncode._similar_unicode_chars:
                similar_chars = BonfireTextEvasionEncode._similar_unicode_chars[
                    char.lower()
                ]
                result.append(random.choice(similar_chars))

        return "".join(result)

    #########################[ end similar_unicode_chars_all ]################################################

    # List of math symbols to use for augmentation
    _math_symbols: List[str] = [
        "+",
        "-",
        "*",
        "/",
        "=",
        "<",
        ">",
        "≈",
        "≠",
        "≤",
        "≥",
        "≡",
        "≈",
        "∞",
        "∑",
        "∏",
        "∫",
    ]

    #########################[ start math_symbols_random ]##############################################
    @staticmethod
    def math_symbols_random(text: str, probability: float = 0.2) -> str:
        """
        Add math symbols to the text with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of adding a math symbol after each character (default: 0.2)

        Returns:
            str: Text with math symbols added
        """
        result = []
        for char in text:
            result.append(char)
            if random.random() < probability:
                result.append(random.choice(BonfireTextEvasionEncode._math_symbols))

        return "".join(result)

    #########################[ end math_symbols_random ]################################################

    #########################[ start math_symbols_all ]##############################################
    @staticmethod
    def math_symbols_all(text: str) -> str:
        """
        Add math symbols after every character in the text.

        Args:
            text: Input text to modify

        Returns:
            str: Text with math symbols added after every character
        """
        result = []
        for char in text:
            result.append(char)
            result.append(random.choice(BonfireTextEvasionEncode._math_symbols))

        return "".join(result)

    #########################[ end math_symbols_all ]################################################

    #########################[ start base64_random ]##############################################
    @staticmethod
    def base64_chars_random(text: str, probability: float = 0.4) -> str:
        """
        Mix Base64 encoded characters into the text with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of replacing each character with a Base64 encoded character (default: 0.4)

        Returns:
            str: Text with Base64 encoded characters mixed in
        """
        result = []
        for char in text:
            if random.random() < probability:
                # Encode the character to Base64 and append
                encoded_char = base64.b64encode(char.encode()).decode()
                result.append(encoded_char)
            else:
                result.append(char)

        return "".join(result)

    #########################[ end base64_random ]################################################

    #########################[ start base64_text_all ]##############################################
    @staticmethod
    def base64_text_all(text: str) -> str:
        """
        Encode the entire text as a single Base64 string.

        Args:
            text: Input text to modify

        Returns:
            str: The entire text encoded as Base64
        """
        return base64.b64encode(text.encode()).decode()

    #########################[ end base64_text_all ]################################################

    #########################[ start base64_words_all ]##############################################
    @staticmethod
    def base64_words_all(text: str) -> str:
        """
        Encode all words in the text to Base64, preserving spaces and punctuation.

        Args:
            text: Input text to modify

        Returns:
            str: Text with all words encoded to Base64
        """
        # Split the text into words while preserving whitespace and punctuation
        pattern = r"(\w+|[^\w\s]+|\s+)"
        tokens = re.findall(pattern, text)
        result = []

        for token in tokens:
            # Only encode actual words, not whitespace or punctuation
            if re.match(r"\w+", token):
                encoded_token = base64.b64encode(token.encode()).decode()
                result.append(encoded_token)
            else:
                result.append(token)

        return "".join(result)

    #########################[ end base64_words_all ]################################################

    #########################[ start base64_words_random ]##############################################
    @staticmethod
    def base64_words_random(text: str, probability: float = 0.5) -> str:
        """
        Randomly encode words in the text to Base64, preserving spaces and punctuation.

        Args:
            text: Input text to modify
            probability: Probability of encoding each word (default: 0.5)

        Returns:
            str: Text with randomly selected words encoded to Base64
        """
        # Split the text into words while preserving whitespace and punctuation
        pattern = r"(\w+|[^\w\s]+|\s+)"
        tokens = re.findall(pattern, text)
        result = []

        for token in tokens:
            # Only potentially encode actual words, not whitespace or punctuation
            if re.match(r"\w+", token) and random.random() < probability:
                encoded_token = base64.b64encode(token.encode()).decode()
                result.append(encoded_token)
            else:
                result.append(token)

        return "".join(result)

    #########################[ end base64_words_random ]################################################

    #########################[ start hex_encoding_random ]##############################################
    @staticmethod
    def hex_encoding_random(text: str, probability: float = 0.4) -> str:
        """
        Mix hex encoded characters into the text with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of replacing each character with a hex encoded character (default: 0.4)

        Returns:
            str: Text with hex encoded characters mixed in
        """
        result = []
        for char in text:
            if random.random() < probability:
                # Encode the character to hex and append
                encoded_char = hex(ord(char))[2:]
                result.append(encoded_char)
            else:
                result.append(char)

        return "".join(result)

    #########################[ end hex_encoding_random ]################################################

    #########################[ start hex_encoding_all ]##############################################
    @staticmethod
    def hex_encoding_all(text: str) -> str:
        """
        Encode all characters in the text to hexadecimal.

        Args:
            text: Input text to modify

        Returns:
            str: Text with all characters encoded as hexadecimal
        """
        result = []
        for char in text:
            # Encode every character to hex and append
            encoded_char = hex(ord(char))[2:]
            result.append(encoded_char)

        return "".join(result)

    #########################[ end hex_encoding_all ]################################################

    #########################[ start binary_encoding_random ]##############################################
    @staticmethod
    def binary_encoding_random(text: str, probability: float = 0.4) -> str:
        """
        Mix binary encoded characters into the text with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of replacing each character with a binary encoded character (default: 0.4)

        Returns:
            str: Text with binary encoded characters mixed in
        """
        result = []
        for char in text:
            if random.random() < probability:
                # Encode the character to binary and append
                encoded_char = bin(ord(char))[2:]  # Remove '0b' prefix
                result.append(encoded_char)
            else:
                result.append(char)

        return "".join(result)

    #########################[ end binary_encoding_random ]################################################

    #########################[ start binary_encoding_all ]##############################################
    @staticmethod
    def binary_encoding_all(text: str) -> str:
        """
        Encode all characters in the text to binary.

        Args:
            text: Input text to modify

        Returns:
            str: Text with all characters encoded as binary
        """
        result = []
        for char in text:
            # Encode every character to binary and append
            encoded_char = bin(ord(char))[2:]  # Remove '0b' prefix
            result.append(encoded_char)

        return "".join(result)

    #########################[ end binary_encoding_all ]################################################

    # Dictionary of HTML entities for various characters
    _html_entities: Dict[str, str] = {
        "a": "&aacute;",
        "b": "&beta;",
        "c": "&copy;",
        "d": "&deg;",
        "e": "&eacute;",
        "f": "&frac12;",
        "g": "&gamma;",
        "h": "&half;",
        "i": "&iacute;",
        "j": "&jmath;",
        "k": "&kappa;",
        "l": "&lambda;",
        "m": "&micro;",
        "n": "&nbsp;",
        "o": "&oacute;",
        "p": "&para;",
        "q": "&quarter;",
        "r": "&raquo;",
        "s": "&sect;",
        "t": "&trade;",
        "u": "&uacute;",
        "v": "&verbar;",
        "w": "&wreath;",
        "x": "&xi;",
        "y": "&yen;",
        "z": "&zeta;",
    }

    #########################[ start html_entities_random ]##############################################
    @staticmethod
    def html_entities_random(text: str, probability: float = 0.4) -> str:
        """
        Mix HTML entities into the text with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of replacing each character with an HTML entity (default: 0.4)

        Returns:
            str: Text with HTML entities mixed in
        """
        result = []
        for char in text:
            if (
                char.lower() in BonfireTextEvasionEncode._html_entities
                and random.random() < probability
            ):
                # Replace the character with an HTML entity
                result.append(BonfireTextEvasionEncode._html_entities[char.lower()])
            else:
                result.append(char)

        return "".join(result)

    #########################[ end html_entities_random ]################################################

    #########################[ start html_entities_all ]##############################################
    @staticmethod
    def html_entities_all(text: str) -> str:
        """
        Replace all eligible characters in the text with HTML entities.

        Args:
            text: Input text to modify

        Returns:
            str: Text with all eligible characters replaced by HTML entities
        """
        result = []
        for char in text:
            if char.lower() in BonfireTextEvasionEncode._html_entities:
                # Replace the character with an HTML entity
                result.append(BonfireTextEvasionEncode._html_entities[char.lower()])
            else:
                result.append(char)

        return "".join(result)

    # List of emojis to use as base for variation selectors
    _emojis = [
        "😀",
        "😁",
        "😂",
        "🤣",
        "😃",
        "😄",
        "😅",
        "😆",
        "😉",
        "😊",
        "😋",
        "😎",
        "😍",
        "😘",
        "🥰",
        "😗",
        "😙",
        "😚",
        "🙂",
        "🤗",
        "🤩",
        "🤔",
        "🤨",
        "😐",
        "😑",
    ]

    #########################[ start _byte_to_variation_selector ]##############################################
    @staticmethod
    def _byte_to_variation_selector(byte: int) -> str:
        """
        Convert a byte value to a Unicode variation selector.

        Args:
            byte: Byte value (0-255)

        Returns:
            str: Unicode variation selector character
        """
        if byte < 16:
            # Use the first range of variation selectors (U+FE00 to U+FE0F)
            return chr(0xFE00 + byte)
        else:
            # Use the second range of variation selectors (U+E0100 to U+E01EF)
            return chr(0xE0100 + (byte - 16))

    #########################[ end _byte_to_variation_selector ]################################################

    #########################[ start emoji_variation_selectors_all ]##############################################
    @staticmethod
    def emoji_variation_selectors_all(text: str) -> str:
        """
        Converts text to bytes and then converts those bytes to Unicode variation selectors
        and appends them to a randomly selected emoji. This creates text that looks like a single emoji but
        contains hidden data in the form of variation selectors.

        Args:
            text: Input text to encode as variation selectors

        Returns:
            str: Emoji with hidden text encoded as variation selectors
        """
        # Randomly select an emoji
        emoji = random.choice(BonfireTextEvasionEncode._emojis)

        # Convert the text to bytes
        text_bytes = text.encode("utf-8")

        # Start with the base emoji
        result = emoji

        # Append variation selectors for each byte
        for byte in text_bytes:
            result += BonfireTextEvasionEncode._byte_to_variation_selector(byte)

        return result

    #########################[ end emoji_variation_selectors_all ]################################################

    #########################[ start emoji_variation_selectors_random ]##############################################
    @staticmethod
    def emoji_variation_selectors_random(text: str, probability: float = 0.5) -> str:
        """
        Converts random words in the text to emoji variation selectors.
        Each selected word is encoded as variation selectors appended to a random emoji.

        Args:
            text: Input text to partially encode as variation selectors
            probability: Probability of encoding each word (default: 0.5)

        Returns:
            str: Text with some words replaced by emojis with hidden data
        """
        words = text.split()
        result = []

        for word in words:
            if random.random() < probability:
                # Encode this word using emoji_variation_selectors_all
                encoded_word = BonfireTextEvasionEncode.emoji_variation_selectors_all(
                    word
                )
                result.append(encoded_word)
            else:
                result.append(word)

        return " ".join(result)

    #########################[ end emoji_variation_selectors_random ]################################################

    _zalgo_chars = [
        "\u0300",
        "\u0301",
        "\u0302",
        "\u0303",
        "\u0304",
        "\u0305",
        "\u0306",
        "\u0307",
        "\u0308",
        "\u0309",
        "\u030a",
        "\u030b",
        "\u030c",
        "\u030d",
        "\u030e",
        "\u030f",
        "\u0310",
        "\u0311",
        "\u0312",
        "\u0313",
        "\u0314",
        "\u0315",
        "\u031a",
        "\u031b",
        "\u033d",
        "\u033e",
        "\u033f",
        "\u0340",
        "\u0341",
        "\u0342",
        "\u0343",
        "\u0344",
        "\u0345",
        "\u0346",
        "\u0347",
        "\u0348",
        "\u0349",
        "\u034a",
        "\u034b",
        "\u034c",
        "\u034d",
        "\u034e",
        "\u034f",
    ]

    #########################[ start zalgo_random ]##############################################
    @staticmethod
    def zalgo_random(text: str, probability: float = 0.4) -> str:
        """
        Add 1-3 zalgo combining marks to random characters in the text with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of adding zalgo marks to each character (default: 0.4)

        Returns:
            str: Text with zalgo characters mixed in
        """
        result = []
        for char in text:
            if random.random() < probability:
                # Add the original character
                result.append(char)
                # Add 1-3 random zalgo combining marks
                num_marks = random.randint(1, 3)
                for _ in range(num_marks):
                    zalgo_mark = random.choice(BonfireTextEvasionEncode._zalgo_chars)
                    result.append(zalgo_mark)
            else:
                result.append(char)

        return "".join(result)

    #########################[ end zalgo_random ]################################################

    #########################[ start zalgo_all ]##############################################
    @staticmethod
    def zalgo_all(text: str) -> str:
        """
        Add 1-3 zalgo combining marks to all characters in the text.

        Args:
            text: Input text to modify

        Returns:
            str: Text with zalgo combining marks added to all characters
        """
        result = []
        for char in text:
            # Add the original character
            result.append(char)
            # Add 1-3 random zalgo combining marks to every character
            num_marks = random.randint(1, 3)
            for _ in range(num_marks):
                zalgo_mark = random.choice(BonfireTextEvasionEncode._zalgo_chars)
                result.append(zalgo_mark)

        return "".join(result)

    #########################[ end zalgo_all ]################################################

    _circled_chars: Dict[str, str] = {
        "a": "ⓐ",
        "b": "ⓑ",
        "c": "ⓒ",
        "d": "ⓓ",
        "e": "ⓔ",
        "f": "ⓕ",
        "g": "ⓖ",
        "h": "ⓗ",
        "i": "ⓘ",
        "j": "ⓙ",
        "k": "ⓚ",
        "l": "ⓛ",
        "m": "ⓜ",
        "n": "ⓝ",
        "o": "ⓞ",
        "p": "ⓟ",
        "q": "ⓠ",
        "r": "ⓡ",
        "s": "ⓢ",
        "t": "ⓣ",
        "u": "ⓤ",
        "v": "ⓥ",
        "w": "ⓦ",
        "x": "ⓧ",
        "y": "ⓨ",
        "z": "ⓩ",
        "A": "Ⓐ",
        "B": "Ⓑ",
        "C": "Ⓒ",
        "D": "Ⓓ",
        "E": "Ⓔ",
        "F": "Ⓕ",
        "G": "Ⓖ",
        "H": "Ⓗ",
        "I": "Ⓘ",
        "J": "Ⓙ",
        "K": "Ⓚ",
        "L": "Ⓛ",
        "M": "Ⓜ",
        "N": "Ⓝ",
        "O": "Ⓞ",
        "P": "Ⓟ",
        "Q": "Ⓠ",
        "R": "Ⓡ",
        "S": "Ⓢ",
        "T": "Ⓣ",
        "U": "Ⓤ",
        "V": "Ⓥ",
        "W": "Ⓦ",
        "X": "Ⓧ",
        "Y": "Ⓨ",
        "Z": "Ⓩ",
        "0": "⓪",
        "1": "①",
        "2": "②",
        "3": "③",
        "4": "④",
        "5": "⑤",
        "6": "⑥",
        "7": "⑦",
        "8": "⑧",
        "9": "⑨",
    }

    #########################[ start circled_random ]##############################################
    @staticmethod
    def circled_random(text: str, probability: float = 0.4) -> str:
        """
        Convert random characters to their Unicode circled equivalents with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of converting each character (default: 0.4)

        Returns:
            str: Text with random characters converted to circled Unicode characters
        """
        result = []
        for char in text:
            if (
                random.random() < probability
                and char in BonfireTextEvasionEncode._circled_chars
            ):
                # Replace with circled character
                result.append(BonfireTextEvasionEncode._circled_chars[char])
            else:
                result.append(char)

        return "".join(result)

    #########################[ end circled_random ]################################################

    #########################[ start circled_all ]##############################################
    @staticmethod
    def circled_all(text: str) -> str:
        """
        Convert all eligible characters to their Unicode circled equivalents.

        Args:
            text: Input text to modify

        Returns:
            str: Text with all eligible characters converted to circled Unicode characters
        """
        result = []
        for char in text:
            if char in BonfireTextEvasionEncode._circled_chars:
                # Replace with circled character
                result.append(BonfireTextEvasionEncode._circled_chars[char])
            else:
                result.append(char)

        return "".join(result)

    #########################[ end circled_all ]################################################

    _bubble_chars: Dict[str, str] = {
        "A": "🅰",
        "B": "🅱",
        "C": "🅲",
        "D": "🅳",
        "E": "🅴",
        "F": "🅵",
        "G": "🅶",
        "H": "🅷",
        "I": "🅸",
        "J": "🅹",
        "K": "🅺",
        "L": "🅻",
        "M": "🅼",
        "N": "🅽",
        "O": "🅾",
        "P": "🅿",
        "Q": "🆀",
        "R": "🆁",
        "S": "🆂",
        "T": "🆃",
        "U": "🆄",
        "V": "🆅",
        "W": "🆆",
        "X": "🆇",
        "Y": "🆈",
        "Z": "🆉",
        "a": "🇦",
        "b": "🇧",
        "c": "🇨",
        "d": "🇩",
        "e": "🇪",
        "f": "🇫",
        "g": "🇬",
        "h": "🇭",
        "i": "🇮",
        "j": "🇯",
        "k": "🇰",
        "l": "🇱",
        "m": "🇲",
        "n": "🇳",
        "o": "🇴",
        "p": "🇵",
        "q": "🇶",
        "r": "🇷",
        "s": "🇸",
        "t": "🇹",
        "u": "🇺",
        "v": "🇻",
        "w": "🇼",
        "x": "🇽",
        "y": "🇾",
        "z": "🇿",
        "0": "⓪",
        "1": "①",
        "2": "②",
        "3": "③",
        "4": "④",
        "5": "⑤",
        "6": "⑥",
        "7": "⑦",
        "8": "⑧",
        "9": "⑨",
        " ": " ",
    }

    #########################[ start bubble_random ]##############################################
    @staticmethod
    def bubble_random(text: str, probability: float = 0.4) -> str:
        """
        Convert random characters to their Unicode fullwidth (bubble) equivalents with a given probability.

        Args:
            text: Input text to modify
            probability: Probability of converting each character (default: 0.4)

        Returns:
            str: Text with random characters converted to fullwidth Unicode characters
        """
        result = []
        for char in text:
            if (
                random.random() < probability
                and char in BonfireTextEvasionEncode._bubble_chars
            ):
                # Replace with bubble character
                result.append(BonfireTextEvasionEncode._bubble_chars[char])
            else:
                result.append(char)

        return "".join(result)

    #########################[ end bubble_random ]################################################

    #########################[ start bubble_all ]##############################################
    @staticmethod
    def bubble_all(text: str) -> str:
        """
        Convert all eligible characters to their Unicode fullwidth (bubble) equivalents.

        Args:
            text: Input text to modify

        Returns:
            str: Text with all eligible characters converted to fullwidth Unicode characters
        """
        result = []
        for char in text:
            if char in BonfireTextEvasionEncode._bubble_chars:
                # Replace with bubble character
                result.append(BonfireTextEvasionEncode._bubble_chars[char])
            else:
                result.append(char)

        return "".join(result)

    #########################[ end bubble_all ]################################################


###################################[ end BonfireTextEvasionEncode ]##############################################

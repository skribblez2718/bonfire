import random
from typing import List, Optional, Dict


###################################[ start BonfireTextEvasionBoN ]###################################
class BonfireTextEvasionBoN:
    """
    Class for Best of N text evasion techniques.
    Contains methods for word scrambling, random capitalization, and character noising.
    """

    #########################[ start word_scrambling_random ]#########################
    @staticmethod
    def word_scrambling_random(text: str, probability: float = 0.6) -> str:
        """
        Randomly scramble individual letters in words.

        Args:
            text: The text to augment
            probability: Probability of scrambling each word (default: 0.6)

        Returns:
            str: The augmented text with scrambled words
        """
        words: List[str] = text.split()
        result: List[str] = []

        for word in words:
            if len(word) <= 3 or random.random() > probability:
                # Don't scramble words that are too short or based on probability
                result.append(word)
            else:
                # Keep first and last letter, scramble the middle
                first: str = word[0]
                middle: List[str] = list(word[1:-1])
                last: str = word[-1]
                random.shuffle(middle)
                scrambled: str = first + "".join(middle) + last
                result.append(scrambled)

        return " ".join(result)

    #########################[ end word_scrambling_random ]###########################

    #########################[ start capitalization_random ]##########################
    @staticmethod
    def capitalization_random(text: str, probability: float = 0.6) -> str:
        """
        Randomly capitalize individual letters in words.

        Args:
            text: The text to augment
            probability: Probability of capitalizing each letter (default: 0.6)

        Returns:
            str: The augmented text with random capitalization
        """
        result: str = ""

        for char in text:
            if char.isalpha() and random.random() < probability:
                # Randomly change the case of alphabetic characters
                if char.islower():
                    result += char.upper()
                else:
                    result += char.lower()
            else:
                result += char

        return result

    #########################[ end capitalization_random ]############################

    #########################[ start character_noising_random ]#######################
    @staticmethod
    def character_noising_random(
        text: str,
        lookalike_prob: float = 0.2,
        ascii_shift_prob: float = 0.06,
        noise_chars: Optional[List[str]] = None,
    ) -> str:
        """
        Randomly replace individual letters in words with other characters using two methods:
        1. Replace with similar looking characters (probability: lookalike_prob)
        2. Shift ASCII value by +/-1 (probability: ascii_shift_prob)

        Args:
            text: The text to augment
            lookalike_prob: Probability of replacing with a lookalike character (default: 0.2)
            ascii_shift_prob: Probability of shifting ASCII value (default: 0.06)
            noise_chars: List of characters to use for replacement. If None, uses similar looking characters.

        Returns:
            str: The augmented text with character noise
        """
        if noise_chars is None:
            # Default similar-looking character replacements
            replacements: Dict[str, List[str]] = {
                "a": ["@", "4", "α", "ä", "å", "ã", "ă", "ą"],
                "b": ["6", "8", "β", "þ", "ƀ", "ɓ"],
                "c": ["(", "<", "¢", "ç", "ć", "č"],
                "d": ["đ", "ď", "ɗ", "ð", "ƌ", "ȡ"],
                "e": ["3", "€", "ε", "è", "é", "ê", "ë", "ĕ"],
                "f": ["ƒ", "ſ", "ʃ", "ʄ", "ɟ", "ʩ"],
                "g": ["9", "6", "ğ", "ģ", "ǧ", "ġ"],
                "h": ["#", "ħ", "ȟ", "ɦ", "ɧ", "ɥ"],
                "i": ["1", "!", "|", "í", "ì", "î", "ï", "ı"],
                "j": ["ĵ", "ɉ", "ʝ", "ɟ", "ʄ", "ǰ"],
                "k": ["κ", "ķ", "ƙ", "ǩ", "ʞ", "ĸ"],
                "l": ["1", "|", "/", "ĺ", "ļ", "ł"],
                "m": ["ɱ", "ɯ", "ɰ", "ɱ", "ʍ", "ḿ"],
                "n": ["η", "ή", "ŋ", "ñ", "ń", "ņ"],
                "o": ["0", "ø", "θ", "ó", "ò", "ô", "ö", "õ"],
                "p": ["ρ", "þ", "ƥ", "ƿ", "ƪ", "ƹ"],
                "q": ["φ", "ʠ", "ɋ", "ʘ", "ǫ", "ɊQ"],
                "r": ["®", "ř", "ŕ", "ŗ", "ɍ", "ɽ"],
                "s": ["5", "$", "ß", "ś", "š", "ş"],
                "t": ["+", "7", "τ", "ţ", "ť", "ŧ"],
                "u": ["μ", "ú", "ù", "û", "ü", "ŭ"],
                "v": ["ν", "υ", "ʋ", "ʌ", "ⱱ", "ⱴ"],
                "w": ["ω", "ώ", "ŵ", "ẁ", "ẃ", "ẅ"],
                "x": ["×", "✗", "✘", "ж", "χ", "ξ"],
                "y": ["¥", "ý", "ÿ", "ŷ", "ƴ", "ȳ"],
                "z": ["ʐ", "ʑ", "ƶ", "ž", "ż", "ź"],
            }
        else:
            # Use custom noise characters
            replacements = {char: noise_chars for char in "abcdefghijklmnopqrstuvwxyz"}

        result: str = ""

        for char in text:
            char_code: int = ord(char)

            # Method 1: Replace with lookalike character
            if char.lower() in replacements and random.random() < lookalike_prob:
                # Replace with a random character from the replacement list
                replacement_options: List[str] = replacements[char.lower()]
                replacement: str = random.choice(replacement_options)
                result += replacement

            # Method 2: Shift ASCII value by +/-1
            elif 32 <= char_code <= 126 and random.random() < ascii_shift_prob:
                # Randomly add or subtract 1 from the ASCII index
                offset: int = random.choice([-1, 1])
                # Ensure we stay within readable ASCII range
                new_code: int = max(32, min(126, char_code + offset))
                result += chr(new_code)

            # No modification
            else:
                result += char

        return result

    #########################[ end character_noising_random ]#########################


###################################[ end BonfireTextEvasionBoN ]#####################################

from typing import Callable, List, Optional, Dict
from tqdm import tqdm

from bonfire.utils.augment import BonfireEvasion
from bonfire.utils.bon import BonfireTextEvasionBoN
from bonfire.utils.language import BonfireTextEvasionLanguage
from bonfire.utils.whitespace import BonfireTextEvasionWhitespace
from bonfire.utils.encode import BonfireTextEvasionEncode
from bonfire.utils.reverse import BonfireTextEvasionReverse
from bonfire.utils.decorate import BonfireTextEvasionDecorate


###################################[ start BonfireTextEvasion ]##############################################
class BonfireTextEvasion(BonfireEvasion):
    """
    Class for text augmentation with various methods to modify text data.
    """

    #########################[ start __init__ ]##############################################
    def __init__(
        self,
        prompts: List[Dict[str, str]],
        output_file_path: Optional[str] = None,
    ) -> None:
        super().__init__(
            data=prompts,
            output_file_path=output_file_path,
        )
        self.name: str = "BonfireTextEvasion"

    #########################[ end __init__ ]################################################

    #########################[ start apply ]##############################################
    def apply(self) -> List[Dict[str, str]]:
        """
        Apply all available augmentation methods to the given data num_iterations times.
        Processes a list of merged prompt objects that contain both instruction and template information.

        Returns:
            List[Dict[str, str]]: List of augmented data in JSONL format
        """
        results = []
        text_methods = self.get_available_methods()

        # Process the list of merged prompt objects
        for prompt_obj in tqdm(self.data, desc="Generating text payloads"):
            intent = prompt_obj["intent"]
            method = prompt_obj["method"]
            method_name = prompt_obj["method_name"]
            prompt_name = prompt_obj["prompt_name"]
            prompt_text = prompt_obj["prompt"]

            # Add completely unaltered prompt first
            results.append(
                {
                    "intent": intent,
                    "method": method,
                    "method_name": method_name,
                    "prompt_name": prompt_name,
                    "augmentation": "None",
                    "original": prompt_text,
                    "prompt": prompt_text,
                }
            )

            for augmentation_method in text_methods:
                augmented_prompt = augmentation_method(prompt_text)

                # Modify data field for methods ending with _all
                data_field = augmented_prompt
                if augmentation_method.__name__.endswith("_all"):
                    data_field = (
                        "Use any or all of your abilities to understand and assist me in the following task.\nTask: "
                        + augmented_prompt
                    )

                results.append(
                    {
                        "intent": intent,
                        "method": method,
                        "method_name": method_name,
                        "prompt_name": prompt_name,
                        "augmentation": augmentation_method.__name__,
                        "original": prompt_text,
                        "prompt": data_field,
                    }
                )

        return results

    #########################[ end apply ]################################################

    #########################[ start get_available_methods ]##############################################
    def get_available_methods(self) -> List[Callable]:
        """
        Get a list of available text augmentation methods.

        Returns:
            List[Callable]: List of available text augmentation methods
        """
        return [
            BonfireTextEvasionBoN.word_scrambling_random,
            BonfireTextEvasionBoN.capitalization_random,
            BonfireTextEvasionBoN.character_noising_random,
            BonfireTextEvasionLanguage.add_diacritics_random,
            BonfireTextEvasionLanguage.add_diacritics_all,
            BonfireTextEvasionLanguage.convert_to_l33t_random,
            BonfireTextEvasionLanguage.convert_to_l33t_all,
            BonfireTextEvasionLanguage.convert_to_futhark_random,
            BonfireTextEvasionLanguage.convert_to_futhark_all,
            BonfireTextEvasionLanguage.convert_to_medieval_random,
            BonfireTextEvasionLanguage.convert_to_medieval_all,
            BonfireTextEvasionLanguage.convert_morse_random,
            BonfireTextEvasionLanguage.convert_morse_all,
            BonfireTextEvasionWhitespace.add_spaces_random,
            BonfireTextEvasionWhitespace.add_spaces_all,
            BonfireTextEvasionWhitespace.add_zero_width_spaces_random,
            BonfireTextEvasionWhitespace.add_zero_width_spaces_all,
            BonfireTextEvasionWhitespace.newline_random,
            BonfireTextEvasionWhitespace.newline_all,
            BonfireTextEvasionEncode.similar_unicode_chars_random,
            BonfireTextEvasionEncode.similar_unicode_chars_all,
            BonfireTextEvasionEncode.math_symbols_random,
            BonfireTextEvasionEncode.math_symbols_all,
            BonfireTextEvasionEncode.base64_chars_random,
            BonfireTextEvasionEncode.base64_text_all,
            BonfireTextEvasionEncode.base64_words_all,
            BonfireTextEvasionEncode.base64_words_random,
            BonfireTextEvasionEncode.hex_encoding_random,
            BonfireTextEvasionEncode.hex_encoding_all,
            BonfireTextEvasionEncode.binary_encoding_random,
            BonfireTextEvasionEncode.binary_encoding_all,
            BonfireTextEvasionEncode.html_entities_random,
            BonfireTextEvasionEncode.html_entities_all,
            BonfireTextEvasionEncode.emoji_variation_selectors_all,
            BonfireTextEvasionEncode.emoji_variation_selectors_random,
            BonfireTextEvasionEncode.zalgo_random,
            BonfireTextEvasionEncode.zalgo_all,
            BonfireTextEvasionEncode.circled_random,
            BonfireTextEvasionEncode.circled_all,
            BonfireTextEvasionEncode.bubble_random,
            BonfireTextEvasionEncode.bubble_all,
            BonfireTextEvasionReverse.sentence_reverse_all,
            BonfireTextEvasionReverse.sentence_reverse_random,
            BonfireTextEvasionReverse.word_reverse_all,
            BonfireTextEvasionReverse.word_reverse_random,
            BonfireTextEvasionReverse.word_upside_down_all,
            BonfireTextEvasionReverse.word_upside_down_random,
            BonfireTextEvasionReverse.char_upside_down_random,
            BonfireTextEvasionReverse.word_mirrored_all,
            BonfireTextEvasionReverse.word_mirrored_random,
            BonfireTextEvasionReverse.char_mirrored_random,
            BonfireTextEvasionDecorate.make_wavy_random,
            BonfireTextEvasionDecorate.make_wavy_all,
            BonfireTextEvasionDecorate.make_strikethrough_random,
            BonfireTextEvasionDecorate.make_strikethrough_all,
            BonfireTextEvasionDecorate.make_fullwidth_random,
            BonfireTextEvasionDecorate.make_fullwidth_all,
            BonfireTextEvasionDecorate.make_wide_space_random,
            BonfireTextEvasionDecorate.make_wide_space_all,
            self.all_random,
        ]

    #########################[ end get_available_methods ]################################################

    #########################[ start all_random ]##############################################
    def all_random(self, text: str) -> str:
        """
        Apply all available random augmentation methods to the given text.
        Only applies methods ending in '_random'.

        Args:
            text: The text to augment

        Returns:
            str: The augmented text with all random methods applied
        """
        # Apply each random method in sequence
        result = text

        # Get all methods ending in '_random' and skip this method itself
        methods = [
            m
            for m in self.get_available_methods()
            if m.__name__.endswith("_random") and m != self.all_random
        ]

        for method in methods:
            result = method(result)

        return result

    #########################[ end all_random ]################################################


###################################[ end BonfireTextEvasion ]##############################################

from typing import Callable, List, Optional, Dict
from tqdm import tqdm

from bonfire.utils.augment import BonfireEvasion
from bonfire.config.config import text_augmentations


###################################[ start BonfireTextEvasion ]###################################
class BonfireTextEvasion(BonfireEvasion):
    """
    Class for text augmentation with various methods to modify text data.
    """

    #########################[ start __init__ ]#########################
    def __init__(
        self,
        prompts: List[Dict[str, str]],
        output_file_path: Optional[str],
    ) -> None:
        super().__init__(
            data=prompts,
            output_file_path=output_file_path,
        )
        self.name: str = "BonfireTextEvasion"

    #########################[ end __init__ ]###########################

    #########################[ start apply ]############################
    def apply(self) -> List[Dict[str, str]]:
        """
        Apply all available augmentation methods to the given data num_iterations times.
        Processes a list of merged prompt objects that contain both instruction and template information.

        Returns:
            List[Dict[str, str]]: List of augmented data in JSONL format
        """
        results = []
        text_methods = self.get_available_text_methods()

        def _make_prompt_result(
            intent, method, method_name, prompt_name, augmentation, original, prompt
        ):
            return {
                "intent": intent,
                "method": method,
                "method_name": method_name,
                "prompt_name": prompt_name,
                "augmentation": augmentation,
                "original": original,
                "prompt": prompt,
            }

        def _apply_augmentations(
            intent, method, method_name, prompt_name, prompt_text, text_methods
        ):
            aug_results = []
            if isinstance(prompt_text, list):
                for augmentation_method in text_methods:
                    augmented_prompts = [augmentation_method(pt) for pt in prompt_text]
                    if augmentation_method.__name__.endswith("_all"):
                        augmented_prompts = [
                            "Use any or all of your abilities to understand and assist me in the following task.\nTask: "
                            + pt
                            for pt in augmented_prompts
                        ]
                    aug_results.append(
                        _make_prompt_result(
                            intent,
                            method,
                            method_name,
                            prompt_name,
                            augmentation_method.__name__,
                            prompt_text,
                            augmented_prompts,
                        )
                    )
            else:
                for augmentation_method in text_methods:
                    augmented_prompt = augmentation_method(prompt_text)
                    data_field = augmented_prompt
                    if augmentation_method.__name__.endswith("_all"):
                        data_field = (
                            "Use any or all of your abilities to understand and assist me in the following task.\nTask: "
                            + augmented_prompt
                        )
                    aug_results.append(
                        _make_prompt_result(
                            intent,
                            method,
                            method_name,
                            prompt_name,
                            augmentation_method.__name__,
                            prompt_text,
                            data_field,
                        )
                    )
            return aug_results

        # Process the list of merged prompt objects
        for prompt_obj in tqdm(self.data, desc="Generating text payloads"):
            intent = prompt_obj["intent"]
            method = prompt_obj["method"]
            method_name = prompt_obj["method_name"]
            prompt_name = prompt_obj["prompt_name"]
            prompt_text = prompt_obj["prompt"]

            # Add completely unaltered prompt (string or list)
            results.append(
                _make_prompt_result(
                    intent,
                    method,
                    method_name,
                    prompt_name,
                    "None",
                    prompt_text,
                    prompt_text,
                )
            )
            # Add augmented prompts
            results.extend(
                _apply_augmentations(
                    intent, method, method_name, prompt_name, prompt_text, text_methods
                )
            )

        return results

    #########################[ end apply ]##############################

    #########################[ start get_available_text_methods ]############
    def get_available_text_methods(self) -> List[Callable]:
        """
        Get a list of available text augmentation methods.

        Returns:
            List[Callable]: List of available text augmentation methods
        """
        text_methods = list(text_augmentations)
        text_methods.append(self.all_random_text_methods)
        return text_methods

    #########################[ end get_available_text_methods ]##############

    #########################[ start all_random_text_methods ]##########
    def all_random_text_methods(self, text: str) -> str:
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
            for m in self.get_available_text_methods()
            if m.__name__.endswith("_random") and m != self.all_random_text_methods
        ]

        for method in methods:
            result = method(result)

        return result

    #########################[ end all_random_text_methods ]############


###################################[ end BonfireTextEvasion ]#####################################

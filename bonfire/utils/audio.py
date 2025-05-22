import httpx
import os
import base64
from tqdm import tqdm

from typing import Callable, Optional, TypeVar, List, Dict

from bonfire.utils.augment import BonfireEvasion
from bonfire.config.config import audio_augmentations, text_augmentations_for

# Define a type for audio data
AudioType = TypeVar("AudioType")


###################################[ start BonfireAudioEvasion ]###################################
class BonfireAudioEvasion(BonfireEvasion):
    """
    Class for audio augmentation with various methods to modify audio data.
    """

    #########################[ start __init__ ]#########################
    def __init__(
        self,
        audio: AudioType,
        output_file_path: str,
        format: str,
        language: str = "en",
    ) -> None:
        super().__init__(
            data=audio,
            output_file_path=output_file_path,
        )
        self.name: str = "BonfireAudioEvasion"
        self.language: str = language
        self.format: str = format

    #########################[ end __init__ ]###########################

    #########################[ start apply ]############################
    def apply(self) -> List[Dict[str, AudioType]]:
        """
        Apply all available augmentation methods to the given data num_iterations times.
        Processes a list of merged prompt objects that contain both instruction and template information.

        Returns:
            List[Dict[str, str]]: List of augmented data in JSONL format
        """
        results = []
        text_methods = self.get_available_text_methods()
        audio_augmentation_methods = self.get_available_audio_methods()

        # Process each merged prompt object
        for prompt_obj in tqdm(self.data, desc="Generating audio payloads"):
            intent = prompt_obj["intent"]
            method = prompt_obj["method"]
            method_name = prompt_obj["method_name"]
            prompt_name = prompt_obj["prompt_name"]
            prompt_text = prompt_obj["prompt"]

            def _make_audio_result(
                intent,
                method,
                method_name,
                prompt_name,
                text_augmentation,
                original_text,
                prompt_text,
                audio_augmentation,
                original_audio,
                augmented_audio,
            ):
                return {
                    "intent": intent,
                    "method": method,
                    "method_name": method_name,
                    "prompt_name": prompt_name,
                    "text_augmentation": text_augmentation,
                    "original_text": original_text,
                    "prompt_text": prompt_text,
                    "audio_augmentation": audio_augmentation,
                    "original_audio": original_audio,
                    "augmented_audio": augmented_audio,
                }

            def _apply_audio_augmentations(
                intent,
                method,
                method_name,
                prompt_name,
                prompt_text,
                text_methods,
                audio_augmentation_methods,
            ):
                aug_results = []
                if isinstance(prompt_text, list):
                    for text_method in text_methods:
                        augmented_prompts = [text_method(pt) for pt in prompt_text]
                        if text_method.__name__.endswith("_all"):
                            augmented_prompts = [
                                "Use any or all of your abilities to understand and assist me in the following task.\nTask: "
                                + pt
                                for pt in augmented_prompts
                            ]
                        audio_base64_list = [
                            self._convert_text_to_audio(pt)[1]
                            for pt in augmented_prompts
                        ]
                        for audio_augmentation_method in audio_augmentation_methods:
                            # Pass base64 to augmentation, expect base64 out (if augmentations expect bytes, adjust here)
                            augmented_audios_base64 = [
                                (
                                    audio_augmentation_method(ab)
                                    if isinstance(audio_augmentation_method(ab), str)
                                    else base64.b64encode(
                                        audio_augmentation_method(base64.b64decode(ab))
                                    ).decode("utf-8")
                                )
                                for ab in audio_base64_list
                            ]
                            aug_results.append(
                                _make_audio_result(
                                    intent,
                                    method,
                                    method_name,
                                    prompt_name,
                                    text_method.__name__,
                                    prompt_text,
                                    augmented_prompts,
                                    audio_augmentation_method.__name__,
                                    audio_base64_list,
                                    augmented_audios_base64,
                                )
                            )
                else:
                    for text_method in text_methods:
                        augmented_prompt = text_method(prompt_text)
                        data_field = augmented_prompt
                        if text_method.__name__.endswith("_all"):
                            data_field = (
                                "Use any or all of your abilities to understand and assist me in the following task.\nTask: "
                                + augmented_prompt
                            )
                        audio_base64 = self._convert_text_to_audio(data_field)[1]
                        for audio_augmentation_method in audio_augmentation_methods:
                            augmented_audio = audio_augmentation_method(audio_base64)
                            if isinstance(augmented_audio, str):
                                augmented_audio_base64 = augmented_audio
                            else:
                                augmented_audio_base64 = base64.b64encode(
                                    augmented_audio
                                ).decode("utf-8")
                            aug_results.append(
                                _make_audio_result(
                                    intent,
                                    method,
                                    method_name,
                                    prompt_name,
                                    text_method.__name__,
                                    prompt_text,
                                    data_field,
                                    audio_augmentation_method.__name__,
                                    audio_base64,
                                    augmented_audio_base64,
                                )
                            )
                return aug_results

            # Add completely unaltered prompt and audio (string or list)
            if isinstance(prompt_text, list):
                original_audio_base64_list = [
                    self._convert_text_to_audio(pt)[1] for pt in prompt_text
                ]
                results.append(
                    _make_audio_result(
                        intent,
                        method,
                        method_name,
                        prompt_name,
                        "None",
                        prompt_text,
                        prompt_text,
                        "None",
                        original_audio_base64_list,
                        original_audio_base64_list,
                    )
                )
            else:
                original_audio_base64 = self._convert_text_to_audio(prompt_text)[1]
                results.append(
                    _make_audio_result(
                        intent,
                        method,
                        method_name,
                        prompt_name,
                        "None",
                        prompt_text,
                        prompt_text,
                        "None",
                        original_audio_base64,
                        original_audio_base64,
                    )
                )
            # Add augmented results
            results.extend(
                _apply_audio_augmentations(
                    intent,
                    method,
                    method_name,
                    prompt_name,
                    prompt_text,
                    text_methods,
                    audio_augmentation_methods,
                )
            )

        return results

    #########################[ end apply ]##############################

    #########################[ start _convert_text_to_audio ]###########
    def _convert_text_to_audio(self, text: str) -> tuple[bytes, str]:
        """
        Convert text to audio using the API.

        Args:
            text: The text to convert to audio

        Returns:
            tuple: (audio_bytes, audio_base64)
        """
        # Convert text to audio
        with httpx.Client(timeout=None) as client:
            response = client.post(
                "http://localhost:5050/v1/audio/speech",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENAI_EDGE_TTS_API_KEY')}",
                    "Content-Type": "application/json",
                },
                json={
                    "input": text,
                    "voice": "echo",
                    "response_format": self.format,
                    "speed": 1.1,
                },
            )

        # Get audio bytes and base64
        audio_bytes = response.content
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        return audio_bytes, audio_base64

    #########################[ end _convert_text_to_audio ]#############

    #########################[ start get_available_text_methods ]#######
    def get_available_text_methods(self) -> List[Callable]:
        """
        Get a list of available text augmentation methods.

        Returns:
            List[Callable]: List of available audio augmentation methods
        """
        available_text_methods = list(text_augmentations_for["audio"])
        available_text_methods.append(self.all_random_text_methods)
        return available_text_methods

    #########################[ end get_available_text_methods ]#########

    #########################[ start get_available_audio_methods ]######
    def get_available_audio_methods(self) -> List[Callable]:
        """
        Get a list of available audio augmentation methods.

        Returns:
            List[Callable]: List of available audio augmentation methods
        """
        avaliable_audio_methods = list(audio_augmentations)
        avaliable_audio_methods.append(self.all_random_audio_methods)
        return avaliable_audio_methods

    #########################[ end get_available_audio_methods ]########

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

    #########################[ start all_random_audio_methods ]#########
    def all_random_audio_methods(self, audio: bytes) -> bytes:
        """
        Apply all available random augmentation methods to the given audio.
        Only applies methods ending in '_random'.

        Args:
            audio: The audio to augment

        Returns:
            bytes: The augmented audio with all random methods applied
        """
        # Apply each random method in sequence
        result = audio

        # Get all methods ending in '_random' and skip this method itself
        methods = [
            m
            for m in self.get_available_audio_methods()
            if m.__name__.endswith("_random") and m != self.all_random_audio_methods
        ]

        for method in methods:
            result = method(result)

        return result

    #########################[ end all_random_audio_methods ]###########


###################################[ end BonfireAudioEvasion ]#####################################

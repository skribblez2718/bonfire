import httpx
import os
import io
import base64
import numpy as np
import random
from tqdm import tqdm

from typing import Callable, Optional, TypeVar, List, Dict
from gtts import gTTS
from pydub import AudioSegment
from pydub.generators import WhiteNoise


from bonfire.utils.augment import BonfireEvasion
from bonfire.utils.bon import BonfireTextEvasionBoN
from bonfire.utils.language import BonfireTextEvasionLanguage
from bonfire.utils.whitespace import BonfireTextEvasionWhitespace
from bonfire.utils.reverse import BonfireTextEvasionReverse

# Define a type for audio data
AudioType = TypeVar("AudioType")


###################################[ start BonfireAudioEvasion ]##############################################
class BonfireAudioEvasion(BonfireEvasion):
    """
    Class for audio augmentation with various methods to modify audio data.
    """

    #########################[ start __init__ ]##############################################
    def __init__(
        self,
        audio: AudioType,
        output_file_path: Optional[str] = None,
        language: str = "en",
        format: str = "mp3",
    ) -> None:
        super().__init__(
            data=audio,
            output_file_path=output_file_path,
        )
        self.name: str = "BonfireAudioEvasion"
        self.language: str = language
        self.format: str = format

    #########################[ end __init__ ]################################################

    #########################[ start apply ]##############################################
    def apply(self) -> List[Dict[str, AudioType]]:
        """
        Apply all available augmentation methods to the given data num_iterations times.
        Processes a list of merged prompt objects that contain both instruction and template information.

        Returns:
            List[Dict[str, str]]: List of augmented data in JSONL format
        """
        results = []
        text_methods = self.get_available_text_methods()

        # Process each merged prompt object
        for prompt_obj in tqdm(self.data, desc="Generating audio payloads"):
            intent = prompt_obj["intent"]
            method = prompt_obj["method"]
            method_name = prompt_obj["method_name"]
            prompt_name = prompt_obj["prompt_name"]
            prompt_text = prompt_obj["prompt"]

            # First, add completely unaltered prompt and audio
            _, original_audio_base64 = self._convert_text_to_audio(prompt_text)

            # Add unaltered prompt with unaltered audio
            results.append(
                {
                    "intent": intent,
                    "method": method,
                    "method_name": method_name,
                    "prompt_name": prompt_name,
                    "text_augmentation": "None",
                    "original_text": prompt_text,
                    "prompt_text": prompt_text,
                    "audio_augmentation": "None",
                    "original_audio": original_audio_base64,
                    "augmented_audio": original_audio_base64,
                }
            )

            for text_augmentation_method in text_methods:
                augmented_prompt = text_augmentation_method(prompt_text)

                # Modify data field for methods ending with _all
                data_field = augmented_prompt
                if text_augmentation_method.__name__.endswith("_all"):
                    data_field = (
                        "Use any or all of your abilities to understand and assist me in the following task.\nTask: "
                        + augmented_prompt
                    )

                # Convert prompt text to audio
                audio_bytes, audio_base64 = self._convert_text_to_audio(data_field)

                # Apply audio augmentation methods
                audio_methods = self.get_available_audio_methods()
                for audio_augmentation_method in audio_methods:
                    augmented_audio = audio_augmentation_method(audio_bytes)

                    results.append(
                        {
                            "intent": intent,
                            "method": method,
                            "method_name": method_name,
                            "prompt_name": prompt_name,
                            "text_augmentation": text_augmentation_method.__name__,
                            "original_text": prompt_text,
                            "prompt_text": data_field,
                            "audio_augmentation": audio_augmentation_method.__name__,
                            "original_audio": audio_base64,
                            "augmented_audio": augmented_audio,
                        }
                    )

        return results

    #########################[ end apply ]################################################

    #########################[ start _convert_text_to_audio ]##############################################
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

    #########################[ end _convert_text_to_audio ]################################################

    #########################[ start get_available_text_methods ]##############################################
    def get_available_text_methods(self) -> List[Callable]:
        """
        Get a list of available text augmentation methods.

        Returns:
            List[Callable]: List of available audio augmentation methods
        """
        return [
            BonfireTextEvasionBoN.word_scrambling_random,
            BonfireTextEvasionBoN.capitalization_random,
            BonfireTextEvasionBoN.character_noising_random,
            BonfireTextEvasionLanguage.add_diacritics_random,
            BonfireTextEvasionLanguage.add_diacritics_all,
            BonfireTextEvasionWhitespace.add_spaces_random,
            BonfireTextEvasionWhitespace.add_spaces_all,
            BonfireTextEvasionWhitespace.add_zero_width_spaces_random,
            BonfireTextEvasionWhitespace.add_zero_width_spaces_all,
            BonfireTextEvasionWhitespace.newline_random,
            BonfireTextEvasionWhitespace.newline_all,
            BonfireTextEvasionReverse.sentence_reverse_all,
            BonfireTextEvasionReverse.sentence_reverse_random,
            BonfireTextEvasionReverse.word_reverse_all,
            BonfireTextEvasionReverse.word_reverse_random,
            self.all_random_text_methods,
        ]

    #########################[ end get_available_text_methods ]################################################

    #########################[ start get_available_audio_methods ]##############################################
    def get_available_audio_methods(self) -> List[Callable]:
        """
        Get a list of available audio augmentation methods.

        Returns:
            List[Callable]: List of available audio augmentation methods
        """
        return [
            self.change_speed,
            self.change_pitch,
            self.change_volume,
            self.add_noise,
            self.all,
        ]

    #########################[ end get_available_audio_methods ]################################################

    #########################[ start change_speed ]##############################################
    def change_speed(self, audio: str | gTTS) -> str:
        """
        Randomly speed up or slow down random segments of the audio.

        Args:
            audio: The audio to augment

        Returns:
            str: Base64 encoded audio in the specified format
        """
        # load into pydub
        seg = self._load_segment(audio)

        # split into a few random segments and resample each
        total_ms = len(seg)
        n = random.randint(3, 6)
        chunk_dur = total_ms // n
        pieces = []
        for i in range(n):
            start = i * chunk_dur
            chunk = seg[start : start + chunk_dur]
            # random speed factor 0.8–1.25×
            factor = random.uniform(0.8, 1.25)
            # change frame_rate to speed up/slow down, then restore
            sped = chunk._spawn(
                chunk.raw_data, overrides={"frame_rate": int(chunk.frame_rate * factor)}
            ).set_frame_rate(chunk.frame_rate)
            pieces.append(sped)
        # append any leftover
        if n * chunk_dur < total_ms:
            pieces.append(seg[n * chunk_dur :])

        new = sum(pieces)
        out = io.BytesIO()
        new.export(out, format=self.format)
        return base64.b64encode(out.getvalue()).decode()

    #########################[ end change_speed ]################################################

    #########################[ start change_pitch ]##############################################
    def change_pitch(self, audio: str | gTTS) -> str:
        """
        Randomly shift pitch (±2 semitones) on random segments.

        Args:
            audio: The audio to augment

        Returns:
            str: Base64 encoded audio in the specified format
        """
        seg = self._load_segment(audio)

        total_ms = len(seg)
        n = random.randint(3, 6)
        chunk_dur = total_ms // n
        pieces = []
        for i in range(n):
            start = i * chunk_dur
            chunk = seg[start : start + chunk_dur]
            # random semitone shift between -2 and +2
            semitones = random.uniform(-2, 2)
            rate_factor = 2 ** (semitones / 12)
            shifted = chunk._spawn(
                chunk.raw_data,
                overrides={"frame_rate": int(chunk.frame_rate * rate_factor)},
            ).set_frame_rate(chunk.frame_rate)
            pieces.append(shifted)
        if n * chunk_dur < total_ms:
            pieces.append(seg[n * chunk_dur :])

        new = sum(pieces)
        out = io.BytesIO()
        new.export(out, format=self.format)
        return base64.b64encode(out.getvalue()).decode()

    #########################[ end change_pitch ]################################################

    #########################[ start change_volume ]##############################################
    def change_volume(self, audio: str | gTTS) -> str:
        """
        Randomly change volume (±6 dB) in random segments.

        Args:
            audio: The audio to augment

        Returns:
            str: Base64 encoded audio in the specified format
        """
        seg = self._load_segment(audio)

        total_ms = len(seg)
        n = random.randint(3, 6)
        chunk_dur = total_ms // n
        pieces = []
        for i in range(n):
            start = i * chunk_dur
            chunk = seg[start : start + chunk_dur]
            # random gain between -6 and +6 dB
            gain = random.uniform(-6, 6)
            pieces.append(chunk.apply_gain(gain))
        if n * chunk_dur < total_ms:
            pieces.append(seg[n * chunk_dur :])

        new = sum(pieces)
        out = io.BytesIO()
        new.export(out, format=self.format)
        return base64.b64encode(out.getvalue()).decode()

    #########################[ end change_volume ]################################################

    #########################[ start add_noise ]##############################################
    def add_noise(self, audio: str | gTTS) -> str:
        """
        Overlay white noise on random portions of the audio.

        Args:
            audio: The audio to augment

        Returns:
            str: Base64 encoded audio in the specified format
        """
        seg = self._load_segment(audio)

        total_ms = len(seg)
        # generate a full-length noise track at -30 dBFS
        noise = WhiteNoise().to_audio_segment(duration=total_ms).apply_gain(-30)

        # choose some random overlay windows
        for _ in range(random.randint(2, 5)):
            start = random.randint(0, total_ms - 1000)
            dur = random.randint(500, 3000)
            seg = seg.overlay(noise[start : start + dur], position=start)

        out = io.BytesIO()
        seg.export(out, format=self.format)
        return base64.b64encode(out.getvalue()).decode()

    #########################[ end add_noise ]################################################

    #########################[ start _load_segment ]##############################################
    def _load_segment(self, audio: str | bytes) -> AudioSegment:
        """
        Load an audio segment from a base64 string or raw bytes.
        Automatically detects the audio format if possible, otherwise uses the specified format.

        Args:
            audio: The audio to load

        Returns:
            AudioSegment: The loaded audio segment
        """
        buf = io.BytesIO()

        if isinstance(audio, (bytes, bytearray)):
            # raw audio bytes → AudioSegment
            buf.write(audio)
        elif isinstance(audio, str):
            # base64‑encoded audio → bytes → AudioSegment
            raw = base64.b64decode(audio)
            buf.write(raw)
        else:
            raise ValueError("Invalid audio type")

        buf.seek(0)
        # Try to detect format from the first few bytes
        header = buf.read(4)
        buf.seek(0)

        # Check for WAV header (RIFF)
        if header.startswith(b"RIFF"):
            detected_format = "wav"
        # Check for MP3 header (ID3 or MPEG frame sync)
        elif header.startswith(b"ID3") or (
            header[0] == 0xFF and (header[1] & 0xE0) == 0xE0
        ):
            detected_format = "mp3"
        else:
            # Use the specified format if detection fails
            detected_format = self.format

        return AudioSegment.from_file(buf, format=detected_format)

    #########################[ start all ]##############################################
    def all(self, audio: AudioType) -> AudioType:
        """
        Apply all available augmentation methods to the given audio.

        Args:
            audio: The audio to augment

        Returns:
            AudioType: The augmented audio with all methods applied
        """
        # Apply each method in sequence
        result = audio

        # Skip the 'all' method itself to avoid infinite recursion
        methods = [m for m in self.get_available_audio_methods() if m != self.all]

        for method in methods:
            result = method(result)

        return result

    #########################[ end all ]################################################

    #########################[ start all_random_text_methods ]##############################################
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

    #########################[ end all_random_text_methods ]################################################


###################################[ end BonfireAudioEvasion ]##############################################

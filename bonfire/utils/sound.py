import io
import base64
import random

from pydub import AudioSegment
from pydub.generators import WhiteNoise


###################################[ start BonfireSoundManipulate ]###################################
class BonfireSoundManipulate:
    """
    Class for sound manipulation with various methods to modify sound data.
    """

    #########################[ start change_speed ]#####################
    @staticmethod
    def change_speed(audio: bytes, format: str = "wav") -> str:
        """
        Randomly speed up or slow down random segments of the audio.

        Args:
            audio: The audio to augment
            format: The format of the audio

        Returns:
            str: Base64 encoded audio in the specified format
        """
        # load into pydub
        seg = BonfireSoundManipulate._load_segment(audio, format)

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
        new.export(out, format=format)
        return base64.b64encode(out.getvalue()).decode()

    #########################[ end change_speed ]#######################

    #########################[ start change_pitch ]#####################
    @staticmethod
    def change_pitch(audio: bytes, format: str = "wav") -> str:
        """
        Randomly shift pitch (±2 semitones) on random segments.

        Args:
            audio: The audio to augment
            format: The format of the audio

        Returns:
            str: Base64 encoded audio in the specified format
        """
        seg = BonfireSoundManipulate._load_segment(audio, format)

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
        new.export(out, format=format)
        return base64.b64encode(out.getvalue()).decode()

    #########################[ end change_pitch ]#######################

    #########################[ start change_volume ]####################
    @staticmethod
    def change_volume(audio: bytes, format: str = "wav") -> str:
        """
        Randomly change volume (±6 dB) in random segments.

        Args:
            audio: The audio to augment
            format: The format of the audio

        Returns:
            str: Base64 encoded audio in the specified format
        """
        seg = BonfireSoundManipulate._load_segment(audio, format)

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
        new.export(out, format=format)
        return base64.b64encode(out.getvalue()).decode()

    #########################[ end change_volume ]######################

    #########################[ start add_noise ]########################
    @staticmethod
    def add_noise(audio: bytes, format: str = "wav") -> str:
        """
        Overlay white noise on random portions of the audio.

        Args:
            audio: The audio to augment
            format: The format of the audio

        Returns:
            str: Base64 encoded audio in the specified format
        """
        seg = BonfireSoundManipulate._load_segment(audio, format)

        total_ms = len(seg)
        # generate a full-length noise track at -30 dBFS
        noise = WhiteNoise().to_audio_segment(duration=total_ms).apply_gain(-30)

        # choose some random overlay windows
        for _ in range(random.randint(2, 5)):
            start = random.randint(0, total_ms - 1000)
            dur = random.randint(500, 3000)
            seg = seg.overlay(noise[start : start + dur], position=start)

        out = io.BytesIO()
        seg.export(out, format=format)
        return base64.b64encode(out.getvalue()).decode()

    #########################[ end add_noise ]##########################

    #########################[ start _load_segment ]####################
    @staticmethod
    def _load_segment(audio: str | bytes, format: str = "wav") -> AudioSegment:
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
            detected_format = format

        return AudioSegment.from_file(buf, format=detected_format)

    #########################[ end _load_segment ]######################


###################################[ end BonfireSoundManipulate ]#####################################

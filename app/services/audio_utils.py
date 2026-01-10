from io import BytesIO
from mutagen import File


def get_audio_duration_seconds(file_bytes: bytes) -> int:
    audio = File(BytesIO(file_bytes))
    if audio is None or not hasattr(audio.info, "length"):
        raise ValueError("Cannot determine audio duration")

    return int(audio.info.length)

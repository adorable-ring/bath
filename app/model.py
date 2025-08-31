from typing import Optional, Dict, Any
from faster_whisper import WhisperModel

_audio = None

def get_audio(audio_size: str = "base"):
    global _audio
    if _audio is None:
        _audio = WhisperModel(audio_size, device="cpu", compute_type="int8")
    return _audio

def transcribe(file_path: str, language: Optional[str] = None, beam_size: int = 1) -> Dict[str, Any]:
    """
    Run speech to text conversion
    Returns {"text": "...", "segments": [...], "language": "en"}
    """
    audio = get_audio()
    segments, info = audio.transcribe(
        file_path,
        language=language,        # None = auto-detect
        beam_size=beam_size,
        vad_filter=True           # helps skip silence
    )
    text = "".join(seg.text for seg in segments)
    return {
        "text": text.strip(),
        "language": info.language,
    }
import io
import pathlib
from fastapi.testclient import TestClient

from app.main import app as fastapi_app
import app.main as main

AUDIO_SAMPLE = pathlib.Path(__file__).parent.parent / "audio" / "voice-sample.mp3"

client = TestClient(fastapi_app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_model_info():
    r = client.get("/model-info")
    assert r.status_code == 200
    data = r.json()
    # Exact values based on app/main.py
    assert data["task"] == "speech-to-text-conversion"
    assert data["framework"] == "faster-whisper (CTranslate2)"
    assert data["model"] == "whisper-base"

def test_transcribe_with_sample(monkeypatch):
    """Use the MP3 file and stub model.transcribe to check file handling."""

    captured = {}

    def sample_transcribe(file_path: str, language=None, beam_size: int = 1):
        captured["file_path"] = file_path
        captured["language"] = language
        captured["beam_size"] = beam_size
        return {"text": "Hi there, this is a sample voice recording created for speech synthesis testing. The quid brown fox jumps over the lazy dog. Just a fun way to include every letter of the alphabet. Numbers like 1, 2, 3 are spoken clearly. Let's see how well this voice captures tone, timing, and natural rhythm. This audio is provided by samplefiles.com.", "language": language or "en"}

    monkeypatch.setattr(main, "transcribe", sample_transcribe)

    with AUDIO_SAMPLE.open("rb") as f:
        files = {"audio": ("voice-sample.mp3", f, "audio/mpeg")}
        data = {"language": "en"}
        r = client.post("/transcribe", files=files, data=data)

    assert r.status_code == 200
    assert r.json() == {"text": "Hi there, this is a sample voice recording created for speech synthesis testing. The quid brown fox jumps over the lazy dog. Just a fun way to include every letter of the alphabet. Numbers like 1, 2, 3 are spoken clearly. Let's see how well this voice captures tone, timing, and natural rhythm. This audio is provided by samplefiles.com.", "language": "en"}
    assert "file_path" in captured


def test_transcribe_missing_file():
    r = client.post("/transcribe", files={}, data={})
    assert r.status_code == 422
    detail = r.json()["detail"]
    assert any(
    ("audio" in err.get("loc", [])) and (err.get("type") in {"missing", "value_error.missing"})
    for err in detail
    )
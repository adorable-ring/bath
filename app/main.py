from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import tempfile
import shutil
from .model import transcribe

app = FastAPI(
    title="Audio to Text Inference Server",
    description="FastAPI service wrapping a Whisper-based speech-to-text model.",
    version="0.1.0",
)

class TranscribeResponse(BaseModel):
    text: str
    language: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_endpoint(
    audio: UploadFile = File(..., description="Audio file (wav, mp3, m4a, flac, etc.)"),
    language: str | None = Form(None),   # optional language hint like "en"
):
    if audio.content_type is None or not audio.filename:
        raise HTTPException(status_code=400, detail="No audio file provided.")

    # Persist to a temporary file for the model
    with tempfile.NamedTemporaryFile(suffix=f"_{audio.filename}", delete=False) as temp:
        with audio.file as f:
            shutil.copyfileobj(f, temp)
        temp_path = temp.name

    result = transcribe(temp_path, language=language)
    return TranscribeResponse(**result)

@app.get("/model-info")
def model_info():
    return {
        "task": "speech-to-text-conversion",
        "framework": "faster-whisper (CTranslate2)",
        "model": "whisper-base",
    }

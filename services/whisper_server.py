from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
import tempfile
import os

app = FastAPI(
    title="Whisper Server",
    version="1.0"
)

print("Loading Whisper model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded.")


@app.get("/")
def root():
    return {
        "service": "Whisper",
        "status": "running"
    }


@app.get("/v1/models")
def models():
    return {
        "object": "list",
        "data": [
            {
                "id": "base",
                "object": "model"
            }
        ]
    }


@app.post("/v1/audio/transcriptions")
async def transcribe(
    file: UploadFile = File(...)
):
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as tmp:

        tmp.write(await file.read())

        temp_path = tmp.name

    segments, info = model.transcribe(
        temp_path
    )

    text = " ".join(
        segment.text
        for segment in segments
    )

    os.remove(temp_path)

    return {
        "text": text.strip(),
        "language": info.language
    }
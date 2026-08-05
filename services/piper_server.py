from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import uuid

from pathlib import Path

app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent.parent
VOICE = BASE_DIR / "voices" / "en_US-lessac-medium.onnx"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


class SpeechRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {
        "service": "Piper",
        "status": "running"
    }


@app.post("/tts")
def synthesize(
    request: SpeechRequest
):

    output = OUTPUT_DIR / f"{uuid.uuid4()}.wav"

    subprocess.run(
        [
            "piper",
            "--model",
            str(VOICE),
            "--output_file",
            str(output),
        ],
        input=request.text.encode(),
        check=True,
    )

    return {
        "audio": str(output)
    }
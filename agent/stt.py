from pathlib import Path
import httpx

from agent.config import WHISPER_URL


async def transcribe(audio_path: Path) -> str:
    """
    Send audio to the local Whisper server
    and return the transcript.
    """

    async with httpx.AsyncClient(timeout=60) as client:

        with open(audio_path, "rb") as audio:

            files = {
                "file": (
                    audio_path.name,
                    audio,
                    "audio/wav",
                )
            }

            response = await client.post(
                f"{WHISPER_URL}/audio/transcriptions",
                files=files,
            )

    response.raise_for_status()

    return response.json()["text"]
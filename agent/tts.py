import httpx
import uuid

from agent.config import PIPER_URL
from pathlib import Path
from livekit.agents import DEFAULT_API_CONNECT_OPTIONS, APIConnectOptions
from livekit.agents import tts as lk_tts


async def speak(text: str):

    async with httpx.AsyncClient() as client:

        response = await client.post(

            f"{PIPER_URL}/tts",

            json={
                "text": text,
            },
        )

    response.raise_for_status()

    return response.json()["audio"]
    

class PiperTTS(lk_tts.TTS):
    def __init__(self):
        super().__init__(
            capabilities=lk_tts.TTSCapabilities(
                streaming=False,
                aligned_transcript=False,
            ),
            sample_rate=22050,
            num_channels=1,
        )

    def synthesize(
        self,
        text: str,
        *,
        conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS,
    ) -> lk_tts.ChunkedStream:
        return PiperChunkedStream(
            tts=self,
            input_text=text,
            conn_options=conn_options,
        )


class PiperChunkedStream(lk_tts.ChunkedStream):
    async def _run(self, output_emitter: lk_tts.AudioEmitter) -> None:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{PIPER_URL}/tts",
                json={"text": self.input_text},
            )

        response.raise_for_status()

        audio_path = Path(response.json()["audio"])
        audio_bytes = audio_path.read_bytes()

        output_emitter.initialize(
            request_id=str(uuid.uuid4()),
            sample_rate=22050,
            num_channels=1,
            mime_type="audio/wav",
        )

        output_emitter.push(audio_bytes)
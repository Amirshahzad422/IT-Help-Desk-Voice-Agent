# agent/tts.py

import httpx

from agent.config import PIPER_URL


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
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
)

from agent.tools import (
    tool_lookup_user,
    tool_create_user,
    tool_unblock_account,
)

from livekit.plugins import openai, silero

from agent.config import (
    OLLAMA_URL,
    OLLAMA_MODEL,
    WHISPER_URL,
)

from agent.prompts import SYSTEM_PROMPT
from agent.tts import PiperTTS

load_dotenv()


class HelpDeskAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=SYSTEM_PROMPT,
            tools=[
                tool_lookup_user,
                tool_create_user,
                tool_unblock_account,
            ],
        )

    async def on_enter(self):
        await self.session.say(
            "Hello. Welcome to Northwind Systems IT Help Desk. How can I help you today?"
        )


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession(
        vad=silero.VAD.load(),

        stt=openai.STT(
            model="base",
            base_url=WHISPER_URL,
            api_key="local",
        ),

        llm=openai.LLM.with_ollama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_URL,
            temperature=0.2,
        ),

        tts=PiperTTS(),
    )

    await session.start(
        room=ctx.room,
        agent=HelpDeskAgent(),
    )


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
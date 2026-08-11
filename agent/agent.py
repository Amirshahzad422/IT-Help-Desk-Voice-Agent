from dotenv import load_dotenv
from agent.db import lookup_user
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
)

from agent.tools import (
    tool_lookup_user,
    create_user_tool_for,
    tool_unblock_account,
)

from livekit.plugins import openai, silero

from agent.config import (
    OLLAMA_URL,
    OLLAMA_MODEL,
    WHISPER_URL,
    MAX_TOKENS,
)

from agent.prompts import SYSTEM_PROMPT
from agent.tts import PiperTTS
from agent.latency import EndToEndLatencyTracker

load_dotenv()


class HelpDeskAgent(Agent):
    def __init__(self, username: str, user: dict | None):
        self.username = username
        self.user = user
        create_user_tool = create_user_tool_for(username)

        available_tools = (
            [tool_lookup_user, tool_unblock_account]
            if user
            else [create_user_tool]
        )

        account_state = (
            "The caller already has the account shown in the initial lookup. "
            "Only discuss account status or unlock it when requested."
            if user
            else
            "This caller has no account yet and is in registration only. "
            "Do not look up, unlock, unblock, reset, or claim to log in to an account. "
            "A successfully created account is Active, so the registration flow ends after creation."
        )

        session_context = (
            f"\nThe signed-in caller username is '{username}'. "
            f"Initial lookup result: {user!r}. "
            "This result is authoritative for the current caller. "
            "Do not ask the caller to repeat their username. "
            + account_state
        )

        super().__init__(
            instructions=SYSTEM_PROMPT + session_context,
            tools=available_tools,
        )

    async def on_enter(self):
        if self.user:
            await self.session.say(
                f"Welcome back, {self.user['full_name']}. "
                "I found your account. What can I help you with?"
            )
        else:
            await self.session.say(
                "Hello, this is Northwind Systems IT Help Desk. "
                f"I don't see an account for username {self.username}. "
                "May I have your full name and email address to get you set up?"
            )


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    participant = await ctx.wait_for_participant()
    username = participant.attributes.get("helpdesk_username", "").strip().lower()
    user = lookup_user(username) if username else None

    session = AgentSession(
    vad=silero.VAD.load(),

    stt=openai.STT(
        model="base",
        base_url=WHISPER_URL,
        api_key="local",
    ),

    llm=openai.LLM(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_URL,
        api_key="ollama",
        temperature=0.2,
        max_completion_tokens=MAX_TOKENS,
        extra_body={
            "options": {
                "num_predict": MAX_TOKENS,
            }
        },
    ),

    tts=PiperTTS(),
    )

    latency_tracker = EndToEndLatencyTracker()

    session.on(
        "user_input_transcribed",
        latency_tracker.on_user_input_transcribed,
    )

    session.on(
        "agent_state_changed",
        latency_tracker.on_agent_state_changed,
    )
    await session.start(
        room=ctx.room,
        agent=HelpDeskAgent(username, user),
    )

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )

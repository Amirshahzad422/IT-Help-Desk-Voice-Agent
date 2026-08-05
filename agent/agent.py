from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
)

load_dotenv()


class HelpDeskAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are Northwind Systems IT Help Desk voice agent. "
                "Help users troubleshoot IT issues clearly and politely."
            )
        )

    async def on_enter(self):
        await self.session.say(
            "Hello. Welcome to Northwind Systems IT Help Desk. How can I help you today?"
        )


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession()

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
import json
from livekit.agents import JobContext


async def emit_account_unblocked_rpc(ctx: JobContext, username: str) -> None:
    payload = json.dumps(
        {
            "event": "account_unblocked",
            "username": username,
            "message": f"Account {username} has been unblocked.",
        }
    )

    for participant in ctx.room.remote_participants.values():
        await ctx.room.local_participant.perform_rpc(
            destination_identity=participant.identity,
            method="account_unblocked",
            payload=payload,
        )
import json
from livekit.agents import JobContext


async def emit_account_unblocked_rpc(
    ctx: JobContext,
    username: str,
) -> None:

    payload = json.dumps({
        "type": "success",
        "message": f"Account {username} has been unblocked.",
    })

    for participant in ctx.room.remote_participants.values():
        try:
            await ctx.room.local_participant.perform_rpc(
                destination_identity=participant.identity,
                method="show_notification",
                payload=payload,
            )

            print(
                f"RPC notification sent to {participant.identity}"
            )

        except Exception as e:
            print(
                f"Failed to send RPC notification "
                f"to {participant.identity}: {e}"
            )
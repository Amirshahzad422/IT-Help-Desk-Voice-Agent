import json


async def emit_account_unblocked_rpc(ctx, username: str) -> None:
    payload = {
        "event": "account_unblocked",
        "username": username,
        "message": f"Account {username} has been unblocked.",
    }

    for participant in ctx.room.remote_participants.values():
        await ctx.room.local_participant.perform_rpc(
            destination_identity=participant.identity,
            method="account_unblocked",
            payload=json.dumps(payload),
        )
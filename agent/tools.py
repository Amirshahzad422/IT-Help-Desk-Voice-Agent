from livekit.agents import function_tool, get_job_context
from agent.rpc import emit_account_unblocked_rpc

from agent.db import (
    lookup_user,
    create_user,
    unblock_account,
)


@function_tool(
    description=(
        "Look up a help desk user by username. "
        "Use this before answering questions about account status."
    )
)
def tool_lookup_user(username: str) -> dict:
    """
    Find a user by username.
    """
    user = lookup_user(username)

    if user is None:
        return {
            "found": False,
            "username": username,
            "message": f"No user found with username {username}.",
        }

    return {
        "found": True,
        "username": user["username"],
        "full_name": user["full_name"],
        "email": user["email"],
        "status": user["status"],
        "message": (
            f"User {user['username']} exists. "
            f"The account status is {user['status']}."
        ),
    }


@function_tool(
    description=(
        "Create a new help desk user after collecting username, full name, and email."
    )
)
def tool_create_user(
    username: str,
    full_name: str,
    email: str,
) -> dict:
    """
    Create a new helpdesk user.
    """
    created = create_user(
        username=username,
        full_name=full_name,
        email=email,
    )

    if created:
        return {
            "created": True,
            "username": username,
            "full_name": full_name,
            "email": email,
            "status": "Active",
            "message": f"User {username} has been created and is Active.",
        }

    return {
        "created": False,
        "username": username,
        "message": (
            f"Could not create user {username}. "
            "The username or email may already exist."
        ),
    }


@function_tool(
    description=(
        "Unblock or unlock a user's account by username. "
        "Use this only after confirming the user exists and their account is locked."
    )
)
async def tool_unblock_account(username: str) -> dict:
    user = lookup_user(username)

    if user is None:
        return {
            "unblocked": False,
            "username": username,
            "message": f"Could not unblock account {username}. User was not found.",
        }

    if user["status"] != "Locked":
        return {
            "unblocked": False,
            "username": user["username"],
            "status": user["status"],
            "message": (
                f"Account {user['username']} is {user['status']}; "
                "only Locked accounts can be unblocked."
            ),
        }

    if not unblock_account(user["username"]):
        return {
            "unblocked": False,
            "username": user["username"],
            "message": "The account could not be unblocked.",
        }

    # Runs only after SQLite successfully changed Locked → Active.
    job_ctx = get_job_context(required=False)
    if job_ctx is not None:
        await emit_account_unblocked_rpc(job_ctx, user["username"])

    return {
        "unblocked": True,
        "username": user["username"],
        "status": "Active",
        "message": f"Account {user['username']} has been unblocked.",
    }
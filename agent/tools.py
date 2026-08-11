from livekit.agents import function_tool, get_job_context
from agent.rpc import emit_account_unblocked_rpc

from agent.db import (
    lookup_user,
    create_user,
    is_valid_email,
    normalize_email,
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


def create_user_tool_for(signed_in_username: str):
    """Return a creation tool that can create only the signed-in caller's account."""

    @function_tool(
        name="tool_create_user",
        description=(
            "Create the signed-in caller's Northwind account. Use only after the "
            "caller has explicitly confirmed their full name and a valid email address. "
            "Set confirmed to true only when the caller says yes to that confirmation."
        ),
    )
    def tool_create_user(
        full_name: str,
        email: str,
        confirmed: bool = False,
        username: str | None = None,
    ) -> dict:
        """Create a confirmed account for the signed-in caller.

        ``username`` is accepted only for compatibility with models that include
        it in a tool call; the signed-in username captured by this tool is always
        used instead.
        """
        if not confirmed:
            return {
                "created": False,
                "reason": "confirmation_required",
                "message": "Ask the caller to confirm the name and email before creating the account.",
            }

        email = normalize_email(email)

        if not is_valid_email(email):
            return {
                "created": False,
                "reason": "invalid_email",
                "message": (
                    "I have your full name. Please provide the email address "
                    "in the form name@example.com."
                ),
            }

        created = create_user(
            username=signed_in_username,
            full_name=full_name,
            email=email,
        )

        if created:
            return {
                "created": True,
                "username": signed_in_username,
                "full_name": full_name,
                "email": email,
                "status": "Active",
                "message": f"User {signed_in_username} has been created and is Active.",
            }

        return {
            "created": False,
            "username": signed_in_username,
            "reason": "username_or_email_exists",
            "message": (
                f"Could not create user {signed_in_username}. "
                "The username or email may already exist."
            ),
        }

    return tool_create_user


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

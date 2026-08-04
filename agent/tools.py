from agent.db import (
    lookup_user,
    create_user,
    unblock_account,
)


def tool_lookup_user(username: str):
    """
    Find a user by username.
    """
    return lookup_user(username)


def tool_create_user(
    username: str,
    full_name: str,
    email: str,
):
    """
    Create a new helpdesk user.
    """
    return create_user(
        username=username,
        full_name=full_name,
        email=email,
    )


def tool_unblock_account(username: str):
    """
    Unlock a user's account.
    """
    return unblock_account(username)
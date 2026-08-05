import sqlite3
from pathlib import Path

# Database path
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "helpdesk.db"


def get_connection():
    """Create and return a SQLite database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def lookup_user(username: str):
    """
    Look up a user by username.
    Returns a dictionary if found, otherwise None.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def create_user(username: str, full_name: str, email: str):
    """
    Create a new user.
    New users are Active by default.
    Returns True if successful, False if username/email already exists.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users
            (username, full_name, email, status)
            VALUES (?, ?, ?, ?)
            """,
            (username, full_name, email, "Active")
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def unblock_account(username: str):
    """
    Change a user's status to Active.
    Returns True if updated successfully.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET status = 'Active'
        WHERE username = ?
        """,
        (username,)
    )

    conn.commit()

    success = cursor.rowcount > 0

    conn.close()

    return success


def update_status(username: str, status: str):
    """
    Update a user's account status.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET status = ?
        WHERE username = ?
        """,
        (status, username)
    )

    conn.commit()

    success = cursor.rowcount > 0

    conn.close()

    return success


def get_all_users():
    """
    Return all users as a list of dictionaries.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
import sqlite3
import re
from pathlib import Path

# Database path
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "helpdesk.db"

# This intentionally accepts ordinary addresses such as name@gmail.com and
# username@example.com, without trying to implement the entire email RFC.
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

def normalize_username(username: str) -> str:
    return username.strip().lower()


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(email.strip()))

def get_connection():
    """Create and return a SQLite database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def lookup_user(username: str):
    username = normalize_username(username)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE lower(trim(username)) = ?",
        (username,),
    )
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def create_user(username: str, full_name: str, email: str):
    username = normalize_username(username)
    full_name = full_name.strip()
    email = email.strip().lower()

    if not username or not full_name or not is_valid_email(email):
        return False

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, full_name, email, status)
            VALUES (?, ?, ?, 'Active')
            """,
            (username, full_name, email),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def unblock_account(username: str):
    username = normalize_username(username)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE users
        SET status = 'Active'
        WHERE lower(trim(username)) = ?
          AND status = 'Locked'
        """,
        (username,),
    )
    conn.commit()
    success = cursor.rowcount == 1
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

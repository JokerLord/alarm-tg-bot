"""Database managing module."""
import sqlite3
import datetime
import argparse
import typing as tp

__connection = None


def get_connection() -> sqlite3.Connection:
    """Get connection to sqlite3 database 'calls.db'."""
    global __connection
    if __connection is None:
        __connection = sqlite3.connect("calls.db", check_same_thread=False)
    return __connection


def init_db(force: bool = False) -> None:
    """
    Initiate sqlite3 database 'calls.db'.

    Database consists of two tables:
        calls (user_id, date_created, date_expired),
        phones (user_id, phone).

    Arguments:
        force (bool): It True, drops tables before creating, it they exist. Default: False.
    """
    conn = get_connection()
    c = conn.cursor()
    if force:
        c.execute("DROP TABLE IF EXISTS calls")
        c.execute("DROP TABLE IF EXISTS phones")
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS calls (
              id INTEGER PRIMARY KEY,
              user_id INTEGER NOT NULL,
              date_created TIMESTAMP,
              date_expired TIMESTAMP
        )
    """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS phones (
              id INTEGER PRIMARY KEY,
              user_id INTEGER NOT NULL,
              phone TEXT
        )
    """
    )
    conn.commit()


def add_call(user_id: int, date_created: datetime.datetime, date_expired: datetime.datetime) -> None:
    """
    Add call into table 'calls'.

    Arguments:
        user_id (int): Bot user id in Telegram.
        date_created (datetime): Call creating time.
        date_expired (datetime): Call expiring time.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO calls (user_id, date_created, date_expired) VALUES (?, ?, ?)",
        (user_id, date_created, date_expired),
    )
    conn.commit()


def add_phone(user_id: int, phone: str) -> None:
    """
    Add user phone into table 'phones'.

    Arguments:
        user_id (int): Bot user id in Telegram.
        phone (str): Bot user phone in Telegram.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO phones (user_id, phone) VALUES (?, ?)", (user_id, phone))


def get_phone(user_id: int) -> tp.Optional[str]:
    """
    Get user phone by his Telegram id.

    Arguments:
        user_id (int): Bot user id in Telegram.

    Returns:
        phone (str, optional): User phone in Telegram.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT phone FROM phones WHERE user_id=?", (user_id,))
    res = c.fetchall()
    if len(res) == 0:
        return None
    return res[0]


def get_phones_to_call(time: datetime.datetime) -> tp.List[str]:
    """
    Get phones from all non-expired calls.

    Arguments:
        time (datetime): Current datetime.

    Returns:
        phones (tp.List[str]): List of phones.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """
        SELECT DISTINCT phone
        FROM phones as a
        JOIN (SELECT * FROM calls WHERE date_expired>?) as b
        ON a.user_id = b.user_id
        """,
        (time,),
    )
    return [phone for (phone,) in c.fetchall()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-create", action="store_true", help="Force recreate db")
    parser.parse_args()
    args = parser.parse_args()
    init_db(force=args.force_create)

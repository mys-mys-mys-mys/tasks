from contextlib import contextmanager
import mysql.connector
from file_work import get_connection_info


@contextmanager
def get_cursor(database: str | None = "dorms", dictionary: bool = True):
    # Yields a database cursor handling transactions and cleanup automatically
    conn_info = get_connection_info()
    if database:
        conn_info["database"] = database
    conn = mysql.connector.connect(**conn_info)
    cursor = conn.cursor(dictionary=dictionary)
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

from contextlib import contextmanager
import psycopg2
from dotenv import dotenv_values

env = dotenv_values(".env")

def connect():
    try:
        connection = psycopg2.connect(
                host = env["HOST"],
                port = env["PORT"],
                database = env["DATABASE"],
                user = env["USER"],
                password = env["PASSWORD"])
        return connection
    except Exception as e:
        print(f"Failed to connect in the database: {e}")

@contextmanager
def get_cursor():
    connection = connect()
    cursor = None
    if connection is None: 
        raise Exception("Can't connect to the database")
    try:
        cursor = connection.cursor()
        yield cursor
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        if (cursor and not cursor.closed):
            cursor.close()

        if (connection and not connection.closed):
            connection.close()

from decouple import config
import psycopg2
from psycopg2.extras import RealDictCursor

POSTGRES_HOST = config("POSTGRES_HOST")
POSTGRES_PORT = config("POSTGRES_PORT")
POSTGRES_DB = config("POSTGRES_DB")
POSTGRES_USER = config("POSTGRES_USER")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")


def get_connection():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )
    return conn


def get_cursor_dict(conn):
    return conn.cursor(cursor_factory=RealDictCursor)

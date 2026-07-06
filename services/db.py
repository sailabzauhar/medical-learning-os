import os

import psycopg2
from psycopg2.pool import SimpleConnectionPool

from dotenv import load_dotenv

load_dotenv()

# ==================================================
# CONNECTION POOL
# ==================================================

_pool = None


def _create_pool():
    global _pool

    if _pool is None:

        _pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=os.getenv("POSTGRES_HOST"),
            port=int(os.getenv("POSTGRES_PORT")),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            sslmode="require",
            connect_timeout=10,
        )

    return _pool


# ==================================================
# GET CONNECTION
# ==================================================

def get_connection():

    try:

        pool = _create_pool()

        return pool.getconn()

    except Exception as e:

        print("\nDatabase connection failed")
        print(e)

        raise


# ==================================================
# RELEASE CONNECTION
# ==================================================

def release_connection(conn):

    try:

        if conn is not None:

            pool = _create_pool()

            pool.putconn(conn)

    except Exception as e:

        print("Error releasing connection")
        print(e)


# ==================================================
# CLOSE POOL
# ==================================================

def close_pool():

    global _pool

    if _pool is not None:

        _pool.closeall()

        _pool = None
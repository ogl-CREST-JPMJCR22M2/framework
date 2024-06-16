from typing import Optional
from psycopg2 import connect, sql
from psycopg2._psycopg import connection, cursor

dsn = {
        "dbname": "offchaindb",
        "user": "postgres",
        "password": "mysecretpassword",
        "port": "5432",
        "host": "localhost",
}

dsn_wsv = {
        "dbname": "iroha_default",
        "user": "postgres",
        "password": "mysecretpassword",
        "port": "5432",
        "host": "localhost",
}

def QUERYexecutor(SQL, db = 'off'):
    conn: Optional[connection] = None
    try:
        if db == 'wsv': conn = connect(**dsn_wsv)
        else : conn = connect(**dsn)

        with conn.cursor() as cur:
            cur.execute(SQL)
            data = cur.fetchall()
            
    finally:
        if conn:
            conn.close()

    return data




def COMMANDexecutor(SQL, db = 'off'):
    conn: Optional[connection] = None
    try:
        if db == 'wsv': conn = connect(**dsn_wsv)
        else : conn = connect(**dsn)

        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(SQL)

    finally:
        if conn:
            conn.close()

from typing import Optional
from psycopg2 import connect, sql
from psycopg2._psycopg import connection, cursor
#from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

dsn = {
    "dbname": "offchainDB",
    "user": "postgres",
    "password": "postgres",
    "port": "5432",
    "host": "localhost",
}

def INSERT_DATA():
    SQL = sql.SQL(
            "INSERT INTO offchainDB (PartsID, TotalEMISSIONS, EMISSIONS) VALUES ({partsid}, {totalemissions}, {emissions})"
            "ON CONFLICT (PartsID)"
            "DO UPDATE SET TotalEMISSIONS={totalemissions}, EMISSIONS={emissions};"
        ).format(
            field = sql.SQL(",").join([
                sql.Identifier()
            ])
        )


conn: Optional[connection] = None
try:
    conn = connect(**dsn)
    conn.autocommit = True

    with conn.cursor() as cur:
        cur: cursor

        

        cur.execute()
finally:
    if conn:
        conn.close()

        
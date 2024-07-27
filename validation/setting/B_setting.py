from typing import Optional
from psycopg2 import connect
from psycopg2._psycopg import connection, cursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

dsn = {
    "dbname": "offchaindb",
    "user": "postgres",
    "password": "mysecretpassword",
    "port": "5432",
    "host": "postgresB",
}

conn: Optional[connection] = None
try:
    conn = connect(**dsn)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    with conn.cursor() as cur:
        cur: cursor

        cur.execute(
            """CREATE TABLE IF NOT EXISTS offchainDB_CFPval(
                    PartsID CHARACTER varying(288),
                    TotalCFP DECIMAL NOT NULL ,
                    CFP DECIMAL NOT NULL ,
                    PRIMARY KEY (PartsID)
            );

            INSERT INTO offchainDB_CFPval VALUES
            ('P03007', '0.0', '8.0'),
            ('P03009', '0.0', '9.0'),
            ('P03013', '0.0', '10.0'),
            ('P04016', '0.0', '11.0'),
            ('P04017', '0.0', '12.0'),
            ('P04023', '0.0', '13.0'),
            ('P04024', '0.0', '14.0'),
            ('P04030', '0.0', '15.0');"""
        )
finally:
    if conn:
        conn.close()

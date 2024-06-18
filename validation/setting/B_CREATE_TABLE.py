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
            """CREATE TABLE IF NOT EXISTS offchainDB_CO2EMISSIONS(
                    PartsID CHARACTER varying(288),
                    TotalEMISSIONS DECIMAL NOT NULL ,
                    EMISSIONS DECIMAL NOT NULL ,
                    PRIMARY KEY (PartsID)
            );

            INSERT INTO offchainDB_CO2EMISSIONS VALUES
            ('P03007', '0.0', '0.0'),
            ('P03009', '0.0', '0.0'),
            ('P03013', '0.0', '0.0'),
            ('P04016', '0.0', '0.0'),
            ('P04017', '0.0', '0.0'),
            ('P04023', '0.0', '0.0'),
            ('P04024', '0.0', '0.0'),
            ('P04030', '0.0', '0.0');"""
        )
finally:
    if conn:
        conn.close()

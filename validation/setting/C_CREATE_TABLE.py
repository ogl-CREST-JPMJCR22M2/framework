from typing import Optional
from psycopg2 import connect
from psycopg2._psycopg import connection, cursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

dsn = {
    "dbname": "offchaindb",
    "user": "postgres",
    "password": "mysecretpassword",
    "port": "5432",
    "host": "postgresC",
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
            ('P03006', '0.0', '16.0'),
            ('P03008', '0.0', '17.0'),
            ('P03012', '0.0', '18.0'),
            ('P04014', '0.0', '19.0'),
            ('P04015', '0.0', '20.0'),
            ('P04018', '0.0', '21.0'),
            ('P04019', '0.0', '22.0'),
            ('P04020', '0.0', '23.0'),
            ('P04021', '0.0', '24.0'),
            ('P04022', '0.0', '25.0'),
            ('P04025', '0.0', '26.0'),
            ('P04026', '0.0', '27.0'),
            ('P04027', '0.0', '28.0'),
            ('P04028', '0.0', '29.0'),
            ('P04029', '0.0', '30.0');"""
        )
finally:
    if conn:
        conn.close()

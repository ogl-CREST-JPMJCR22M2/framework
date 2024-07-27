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
            ('P03006', '0.0', '3.4'),
            ('P03008', '0.0', '6.7'),
            ('P03009', '0.0', '7.9'),
            ('P04014', '0.0', '2.6'),
            ('P04015', '0.0', '8.0'),
            ('P04018', '0.0', '9.1'),
            ('P04019', '0.0', '5.5'),
            ('P04020', '0.0', '4.3'),
            ('P04021', '0.0', '7.6'),
            ('P04022', '0.0', '3.8'),
            ('P04025', '0.0', '6.2'),
            ('P04026', '0.0', '5.1'),
            ('P04027', '0.0', '8.3'),
            ('P04028', '0.0', '4.9'),
            ('P04029', '0.0', '7.4'),
            ('P05033', '0.0', '2.2'),
            ('P05036', '0.0', '6.5'),
            ('P05037', '0.0', '8.7'),
            ('P05038', '0.0', '3.1'),
            ('P05039', '0.0', '9.2'),
            ('P06053', '0.0', '4.6'),
            ('P06054', '0.0', '5.8'),
            ('P06060', '0.0', '7.3'),
            ('P06061', '0.0', '2.7'),
            ('P06062', '0.0', '8.9'),
            ('P06067', '0.0', '6.0'),
            ('P06068', '0.0', '9.5'),
            ('P06073', '0.0', '3.3'),
            ('P06074', '0.0', '4.4'),
            ('P06075', '0.0', '5.7'),
            ('P07078', '0.0', '9.0'),
            ('P07079', '0.0', '6.2'),
            ('P07084', '0.0', '2.9'),
            ('P07085', '0.0', '7.8'),
            ('P07090', '0.0', '4.1'),
            ('P07091', '0.0', '8.6'),
            ('P07096', '0.0', '3.5'),
            ('P07097', '0.0', '9.3');"""
        )
finally:
    if conn:
        conn.close()

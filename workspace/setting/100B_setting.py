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
            ('P03007', '0.0', '4.5'),
            ('P04023', '0.0', '7.2'),
            ('P04024', '0.0', '6.8'),
            ('P05034', '0.0', '5.1'),
            ('P05035', '0.0', '8.4'),
            ('P05044', '0.0', '3.3'),
            ('P05045', '0.0', '2.7'),
            ('P06056', '0.0', '9.0'),
            ('P06057', '0.0', '6.2'),
            ('P06064', '0.0', '7.8'),
            ('P06065', '0.0', '4.3'),
            ('P06066', '0.0', '3.5'),
            ('P07076', '0.0', '5.7'),
            ('P07077', '0.0', '8.1'),
            ('P07082', '0.0', '2.9'),
            ('P07083', '0.0', '9.3'),
            ('P07088', '0.0', '4.1'),
            ('P07089', '0.0', '5.6'),
            ('P07094', '0.0', '7.4'),
            ('P07095', '0.0', '6.9'),
            ('P07100', '0.0', '1.2');"""
        )
finally:
    if conn:
        conn.close()

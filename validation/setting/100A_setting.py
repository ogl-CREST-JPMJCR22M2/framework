from typing import Optional
from psycopg2 import connect
from psycopg2._psycopg import connection, cursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

dsn = {
    "dbname": "offchaindb",
    "user": "postgres",
    "password": "mysecretpassword",
    "port": "5432",
    "host": "postgresA",
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
            ('P01001', '0.0', '1.5'),
            ('P02002', '0.0', '2.3'),
            ('P02003', '0.0', '4.7'),
            ('P02004', '0.0', '3.8'),
            ('P03005', '0.0', '5.2'),
            ('P03010', '0.0', '6.1'),
            ('P03011', '0.0', '7.4'),
            ('P05031', '0.0', '8.2'),
            ('P05032', '0.0', '9.0'),
            ('P05041', '0.0', '2.7'),
            ('P05042', '0.0', '5.9'),
            ('P05046', '0.0', '3.4'),
            ('P05047', '0.0', '8.7'),
            ('P05051', '0.0', '4.8'),
            ('P05052', '0.0', '6.5'),
            ('P06055', '0.0', '2.1'),
            ('P06058', '0.0', '7.9'),
            ('P06059', '0.0', '9.4'),
            ('P06062', '0.0', '1.8'),
            ('P06063', '0.0', '4.9'),
            ('P06068', '0.0', '3.2'),
            ('P06069', '0.0', '8.3'),
            ('P06074', '0.0', '2.9'),
            ('P06075', '0.0', '6.7'),
            ('P07080', '0.0', '4.6'),
            ('P07081', '0.0', '7.3'),
            ('P07086', '0.0', '5.8'),
            ('P07087', '0.0', '9.1'),
            ('P07092', '0.0', '3.7'),
            ('P07093', '0.0', '2.5'),
            ('P07098', '0.0', '8.4'),
            ('P07099', '0.0', '9.7');"""
        )
finally:
    if conn:
        conn.close()

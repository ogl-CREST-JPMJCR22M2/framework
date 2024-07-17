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
            """CREATE TABLE IF NOT EXISTS offchainDB_CO2EMISSIONS(
                    PartsID CHARACTER varying(288),
                    TotalEMISSIONS DECIMAL NOT NULL ,
                    EMISSIONS DECIMAL NOT NULL ,
                    PRIMARY KEY (PartsID)
            );

            INSERT INTO offchainDB_CO2EMISSIONS VALUES
            ('P01001', '0.0', '1.0'), 
            ('P02002', '0.0', '2.0'),
            ('P02003', '0.0', '3.0'),
	        ('P02004', '0.0', '4.0'),
            ('P03005', '0.0', '0.0'),
            ('P03010', '0.0', '0.0'),
            ('P03011', '0.0', '0.0');"""
        )
finally:
    if conn:
        conn.close()

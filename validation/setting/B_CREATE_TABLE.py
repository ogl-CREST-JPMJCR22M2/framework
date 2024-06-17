from typing import Optional
from psycopg2 import connect
from psycopg2._psycopg import connection, cursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

dsn = {
    "dbname": "offchaindb",
    "user": "postgres",
    "password": "postgres",
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
            ('P01001', '0.0', '0.0'), 
            ('P02002', '0.0', '0.0'),
            ('P02003', '0.0', '0.0'),
	        ('P02004', '0.0', '0.0'),
            ('P03005', '0.0', '0.0'),
            ('P03006', '0.0', '0.0'),
            ('P03007', '0.0', '0.0'),
            ('P03008', '0.0', '0.0'),
            ('P03009', '0.0', '0.0'),
            ('P03010', '0.0', '0.0'),
            ('P03011', '0.0', '0.0'),
            ('P03012', '0.0', '0.0'),
            ('P03013', '0.0', '0.0'),
            ('P04014', '0.0', '0.0'),
            ('P04015', '0.0', '0.0'),
            ('P04016', '0.0', '0.0'),
            ('P04017', '0.0', '0.0'),
            ('P04018', '0.0', '0.0'),
            ('P04019', '0.0', '0.0'),
            ('P04020', '0.0', '0.0'),
            ('P04021', '0.0', '0.0'),
            ('P04022', '0.0', '0.0'),
            ('P04023', '0.0', '0.0'),
            ('P04024', '0.0', '0.0'),
            ('P04025', '0.0', '0.0'),
            ('P04026', '0.0', '0.0'),
            ('P04027', '0.0', '0.0'),
            ('P04028', '0.0', '0.0'),
            ('P04029', '0.0', '0.0'),
            ('P04030', '0.0', '0.0');"""
        )
finally:
    if conn:
        conn.close()

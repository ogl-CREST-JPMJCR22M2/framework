from typing import Optional
from psycopg2 import connect
from psycopg2._psycopg import connection, cursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

args = "C"

for arg in args:

    conn: Optional[connection] = None

    host = "postgres" + arg

    dsn = {
    "dbname": "offchaindb",
    "user": "postgres",
    "password": "mysecretpassword",
    "port": "5432",
    "host": host ,
    }

    try:
        conn = connect(**dsn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with conn.cursor() as cur:
            cur: cursor

            cur.execute(
                """
                
                drop table offchaindb_cfpval;
                
                CREATE TABLE IF NOT EXISTS partinfo(
                        PartID CHARACTER varying(288)
                );

                insert into partinfo values ('P00003');

                CREATE TABLE IF NOT EXISTS CFPval(
                        PartID CHARACTER varying(288),
                        TotalCFP DECIMAL NOT NULL ,
                        CFP DECIMAL NOT NULL
                );

                insert into CFPval values ('P00003', 0.3, 0.3);
                """
            )
            
    finally:
        if conn:
            conn.close()

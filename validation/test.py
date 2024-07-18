from typing import Optional
from psycopg2 import connect
from psycopg2._psycopg import connection, cursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

dsn = {
    "dbname": "testdb",
    "user": "postgres",
    "password": "mysecretpassword",
    "port": "5432",
    "host": "postgresA",
}

def QUERYexecutor(SQL):
    conn: Optional[connection] = None
    try:
        conn = connect(**dsn)
        with conn.cursor() as cur:
            cur.execute(SQL)
            for data in cur:
                print(data)
            #data = cur.fetchall()

    finally:
        if conn:
            conn.close()

    #return data

def COMMANDexecutor(SQL):
    conn: Optional[connection] = None
    try:
        conn = connect(**dsn)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(SQL)

    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    SQL_ok = """
            select dblink_connect('connA','host=postgresA port=5432 dbname=offchaindb user=postgres password=mysecretpassword');
            select * from dblink('connA', 'select partsid, emissions from offchaindb_co2emissions') 
            as connA(partsid CHARACTER varying(288), EMISSIONS DECIMAL);
        """
    SQL_ok2 = """
            select * from dblink(
            'host=postgresA port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
            'select partsid, emissions from offchaindb_co2emissions') 
            as t1(partsid CHARACTER varying(288), EMISSIONS DECIMAL);
        """
    SQL = """
            WITH
                import_tableA AS
                (
                    select * from dblink(
                    'host=postgresA port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
                    'select partsid, emissions from offchaindb_co2emissions') 
                    as t1(partsid CHARACTER varying(288), EMISSIONS DECIMAL)

                ),
                import_tableB AS
               (
                     select * from dblink(
                    'host=postgresB port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
                    'select partsid, emissions from offchaindb_co2emissions') 
                    as t1(partsid CHARACTER varying(288), EMISSIONS DECIMAL)
                ),
                union_tableAB AS(
                    select * from import_tableA
                    union
                    select * from import_tableB      
                ),
                update_table AS
                (
                    update co2emissions set emissions = 1.1
                    where partsid = 'P01001'
                    returning *
                )
                select emissions from union_tableAB where partsid = 'P01001'
        """

    QUERYexecutor(SQL)
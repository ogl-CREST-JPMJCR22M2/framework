from typing import Optional
from psycopg2 import connect, sql
from psycopg2._psycopg import connection, cursor

dsn = {
        "dbname": "test",
        "user": "postgres",
        "password": "mysecretpassword",
        "port": "5432",
        "host": "localhost",
}

def QUERYexecutor(SQL):
    conn: Optional[connection] = None
    try:
        conn = connect(**dsn)

        with conn.cursor() as cur:
            cur.execute(SQL)
            data = cur.fetchall()
            
    finally:
        if conn:
            conn.close()

    return data


def get_TotalEMISSIONS(partsid):

    SQL = sql.SQL("""
            SELECT totalemissions FROM co2emissions WHERE partsid = {PartsID};
        """).format(
            PartsID = sql.Literal(partsid)
        )

    return QUERYexecutor(SQL)[0][0]

def get_ChlidParts(partsid):

    SQL = sql.SQL("""
            SELECT childpartsid FROM co2emissions WHERE partsid = {PartsID};
        """).format(
            PartsID = sql.Literal(partsid)
        )

    return QUERYexecutor(SQL)[0][0]

def quickly_calculate_totalemissions(partsid):
    childpartsid = get_ChlidParts(partsid)
    
    if not childpartsid :
        return get_TotalEMISSIONS(partsid)
    else :
        data =  0
        for i in range(len(childpartsid)):
            data += calculate_totalemissions(childpartsid[i])
        return data


### コマンドの呼び出しを再帰なしで書く

def non_recursion(partsid):
    childpartsid = get_ChlidParts(partsid)
    datalink = get_DataLink(partsid, peer)
    emissions = get_EMISSIONS(partsid, datalink)

    if not childpartsid :
        return IROHA_COMMANDexecutor(partsid, emissions, '0.0', datalink, 'admin@test')
    else : 
        return data + 

    
    


if __name__ == '__main__':

    #insert_data(partsid, totalemissions, emissions)

    quickly_calculate_totalemissions('P01001')
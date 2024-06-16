from typing import Optional
from psycopg2 import connect, sql
from psycopg2._psycopg import connection, cursor

dsn = {
        "dbname": "test",
        "user": "horiharuka",
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

    return QUERYexecutor(SQL, db)[0][0]

def get_childparts(partsid):

    SQL = sql.SQL("""
            SELECT childpartsid FROM co2emissions WHERE partsid = {PartsID};
        """).format(
            PartsID = sql.Literal(partsid)
        )

    return SQLexe.QUERYexecutor(SQL, 'wsv')[0][0]


def calculate_totalemissions(partsid):

    if partsid == 'Nan':
        """ TotalEmissionの再計算 """
        print(partsid)
        return 0
        #return IROHA_COMMANDexecutor(partsid, emissions, sum_child_emissions, 'admin@test') # コマンドによる再計算
    else :
        childpartsid = get_childparts(partsid)
        for i in range(len(childpartsid)) : # child_totalEmissionの取得と合計
            calculate_totalemissions(childpartsid[i])
            sum_child_emissions += get_TotalEMISSIONS(childpartsid[i]) 
            


if __name__ == '__main__':

    #insert_data(partsid, totalemissions, emissions)

    calculate_totalemissions('P01001')
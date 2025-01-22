import commons as common
import time
import csv
import psutil
import SQLexecutor as SQLexe
from psycopg2 import sql


def test():  #peer:executing peer

    SQL = sql.SQL("""
            WITH 
get_childparts AS
(
    WITH RECURSIVE calcu(child_partsid, parents_partsid, duplicates) AS
    (
        SELECT PartsInfo.partsid, PartsInfo.parents_partsid, duplicates
        FROM PartsInfo
        WHERE PartsInfo.parents_partsid = 'P0'
        UNION ALL
        SELECT PartsInfo.partsid, calcu.parents_partsid, PartsInfo.duplicates
        FROM PartsInfo, calcu
        WHERE PartsInfo.parents_partsid = calcu.child_partsid 
    )
    SELECT child_partsid, duplicates
    FROM calcu
),
import_table AS (
    SELECT * FROM dblink(
        'host=postgresA port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
        'SELECT partsid, cfp FROM offchaindb_cfpval') 
        AS t1(partsid CHARACTER varying(288), cfp DECIMAL)
    UNION ALL
    SELECT * FROM dblink(
        'host=postgresB port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
        'SELECT partsid, cfp FROM offchaindb_cfpval') 
        AS t1(partsid CHARACTER varying(288), cfp DECIMAL)
    UNION ALL
    SELECT * FROM dblink(
        'host=postgresC port=5432 dbname=offchaindb user=postgres password=mysecretpassword', 
        'SELECT partsid, cfp FROM offchaindb_cfpval') 
        AS t1(partsid CHARACTER varying(288), cfp DECIMAL)
),
get_totalcfp AS
(   
    SELECT sum(cfp * duplicates) as child_totalcfp
    FROM import_table INNER JOIN get_childparts ON get_childparts.child_partsid = import_table.partsid
), 
new_quantity AS
    (
        SELECT cfp, child_totalcfp + cfp as new_Totalcfp
        FROM get_totalcfp, import_table
        WHERE import_table.partsid = 'P0'
    )
SELECT new_Totalcfp FROM new_quantity;
        """)
    return SQLexe.QUERYexecutor_wsv(SQL, 'postgresA')[0][0]

if __name__ == '__main__':

    sumval = 0.0

    for n in range(10):
        start = time.time()
        test()
        #simplified_validation(partsid,'postgresA')

        t = time.time() - start
        sumval+= t
        #time_data.append([t])
    
    print(sumval/10.0)

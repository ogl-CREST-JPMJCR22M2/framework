import commons as common
import time
import csv
import psutil
import SQLexecutor as SQLexe
from psycopg2 import sql

def naive_validation(partsid, peer):

    datalink = common.get_DataLink(partsid, peer)

    offdb_value = common.get_offchaindb_totalcfp(partsid, datalink) # Comparison destination : values in WSV

    common.IROHA_COMMANDexecutor(partsid,'SetAccountDetail', peer)
    wsv_value = common.get_wsv_totalcfp(partsid, peer) # Comparison source : values in offchainDB

    if float(wsv_value) != float(offdb_value):
        print("Validation Failed")
    else :
        print("Validation Successful")


def simplified_validation(partsid, peer):

    datalink = common.get_DataLink(partsid, peer)

    offdb_totacfp = common.get_offchaindb_totalcfp(partsid, datalink) # Comparison destination : values in WSV
    offdb_cfp = common.get_offchaindb_cfp(partsid, datalink)

    if offdb_cfp < 0 or offdb_cfp > 1000:
        print("Faild Stateful Validation (cfp in offchainDB)")
        return 0

    SQL = sql.SQL("""
        WITH   
           general_table AS
            (   
                SELECT * FROM cfpval
                NATURAL RIGHT JOIN PartsInfo
            )
        SELECT parents_partsid, SUM(totalcfp) AS child_totalcfp
            FROM general_table
            WHERE parents_partsid = {partsid}
            GROUP BY parents_partsid;
        """).format(
            partsid = sql.Literal(partsid)
        )
    child_totalCFP =  SQLexe.QUERYexecutor_wsv(SQL, peer)[0][1]

    if child_totalCFP < 0:
        print("Faild Stateful Validation (chilid totalCFP)")
        return 0
    
    new_totalcfp = child_totalCFP + offdb_cfp

    # if new_totalcfp > (2 ^ 256) / (10 ^ 10):
    #     print("Faild Stateful Validation (overflow new totalcfp)")
    #    return 0

    print(new_totalcfp)
        
    if float(new_totalcfp) != float(offdb_totacfp):
        print("Validation Failed")
    else :
        print("Validation Successful")


if __name__ == '__main__':

    simplified_validation('P00001','postgresA')

    """
    time_data = []
    cpu_list = []
    partsid = ['P09841','P03280','P01093','P00364','P00121', 'P00040','P00013', 'P00004', 'P00001']
    #partsid = 'P03280'
    #filename = 'results_naive'
   
    for pid in partsid:
        #time_data.append([pid, pid])
        start = time.time()
        naive_validation(pid,'postgresA') 
        t = time.time() - start
        time_data.append([t])
    
    for times in time_data:
        print(times)

    
    partsid = 'P00001'
    filename = partsid

    for n in range(100):
        start = time.time()
        naive_validation(partsid,'postgresA')

        t = time.time() - start
        time_data.append([t])
    

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(time_data)
    
    print(f'Data has been written to {filename}')
    """
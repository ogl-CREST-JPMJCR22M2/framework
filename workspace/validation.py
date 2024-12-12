import commons as common
import time
import csv
import psutil

def naive_validation(partsid, peer):

    datalink = common.get_DataLink(partsid, peer)

    offdb_value = common.get_offchaindb_totalcfp(partsid, datalink) # Comparison destination : values in WSV

    common.IROHA_COMMANDexecutor(partsid,'SetAccountDetail', peer)
    wsv_value = common.get_wsv_totalcfp(partsid, peer) # Comparison source : values in offchainDB

    if float(wsv_value) != float(offdb_value):
        print("Validation Failed")
    #else :
    #    print("Validation Successful")


def simplified_validation(partsid, peer):

    datalink = common.get_DataLink(partsid, peer)

    offdb_value = common.get_offchaindb_totalcfp(partsid, datalink) # Comparison destination : values in WSV

    common.IROHA_COMMANDexecutor(partsid,'SubtractAssetQuantity', peer)
    wsv_value = common.get_wsv_totalcfp(partsid, peer) # Comparison source : values in offchainDB

    if float(wsv_value) != float(offdb_value):
        print("Validation Failed")
    #else :
    #    print("Validation Successful")

if __name__ == '__main__':

    time_data = []
    cpu_list = []
    partsid = ['P00040','P00013', 'P00004', 'P00001']
    #partsid = ['P09841','P03280','P01093','P00364','P00121', 'P00040','P00013', 'P00004', 'P00001']
    #partsid = 'P03280'
    #filename = 'results_naive'

    #naive_validation(partsid,'postgresA')    

    
    for pid in partsid:
        #time_data.append([pid, pid])
        if pid == 'P00040':
            for n in range(723):
                simplified_validation(pid,'postgresA')
        else:
            for n in range(1000):
                simplified_validation(pid,'postgresA')
            #start = time.time()
            #t = time.time() - start
            #time_data.append([t])

    """
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
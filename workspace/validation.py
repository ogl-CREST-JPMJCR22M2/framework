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


def quick_validation(partsid, peer):

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
    partsid = ['P09841','P03280','P01093','P00364','P00121', 'P00040','P00013', 'P00001']
    filename = partsid

    for id in partsid:
        time_data.append([partsid, partsid])
        for n in range(100):
            start = time.time()
            naive_validation(partsid,'postgresA')

            t = time.time() - start
            virtual_memory_usage = psutil.virtual_memory().percent
            time_data.append([t, virtual_memory_usage])
            #time.sleep(interval)

    """
    partsid = 'P00001'
    filename = partsid

    for n in range(100):
        start = time.time()
        naive_validation(partsid,'postgresA')

        t = time.time() - start
        time_data.append([t])
    """

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(time_data)
    
    print(f'Data has been written to {filename}')

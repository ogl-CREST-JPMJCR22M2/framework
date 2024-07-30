import commons as common
import time

def naive_validation(partsid, peer):

    datalink = common.get_DataLink(partsid, peer)

    offdb_value = common.get_offchaindb_totalcfp(partsid, datalink) # Comparison destination : values in WSV

    common.IROHA_COMMANDexecutor(partsid,'SetAccountDetail', peer)
    wsv_value = common.get_wsv_totalcfp(partsid, peer) # Comparison source : values in offchainDB

    print("offdb_value", offdb_value)
    print("wsv_value", wsv_value)

    if float(wsv_value) != float(offdb_value):
        print("Validation Failed")
    else :
        print("Validation Successful")


def quick_validation(partsid, peer):

    datalink = common.get_DataLink(partsid, peer)

    offdb_value = common.get_offchaindb_totalcfp(partsid, datalink) # Comparison destination : values in WSV

    common.IROHA_COMMANDexecutor(partsid,'SubtractAssetQuantity', peer)
    wsv_value = common.get_wsv_totalcfp(partsid, peer) # Comparison source : values in offchainDB

    print("offdb_value", offdb_value)
    print("wsv_value", wsv_value)

    if float(wsv_value) != float(offdb_value):
        print("Validation Failed")
    else :
        print("Validation Successful")


if __name__ == '__main__':

    start = time.time()

    partsid = 'P01001'
    naive_validation(partsid,'postgresA')

    t = time.time() - start
    print(t)
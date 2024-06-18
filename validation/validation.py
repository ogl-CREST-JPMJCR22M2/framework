import common
import sys #コマンドライン変数


##############################################
## more quickly validation using WSV values ##
##############################################

def more_quickly_validation(partsid, peer):
    wsv_value = common.get_TotalEMISSIONS(partsid, 'wsv', peer) # 比較先:WSV上の値
    offdb_value = common.get_TotalEMISSIONS(partsid, 'off', peer) # 比較元:offchainDB上の値

    if wsv_value != offdb_value:
        print("Validation Failed")
    else :
        print("Validation Successful")


########################################################
## quickly validation using child_parts in WSV values ##
########################################################

def quickly_validation(partsid, peer):
    offdb_value = common.get_TotalEMISSIONS(partsid, 'off', peer) # 比較元:offchainDB上の値

    # calculating child_totalEmission with WSV values
    child_partsid = common.get_ChlidParts(partsid, peer) # 下位部品のPartsIDの取得
    sum_child_emissions = 0
    for i in range(len(childpartsid)) : # child_totalEmissionの取得と合計
        sum_child_emissions += common.get_TotalEMISSIONS(i, 'wsv', peer) 
    
    # calculating TotalEmissions
    emissions = common.get_TotalEMISSIONS(partsid, 'wsv', peer) # child_totalEmissionの取得と合計
    common.IROHA_COMMANDexecutor(partsid, emissions, sum_child_emissions, 'admin@test') # コマンドによる再計算

    #validation
    wsv_value = common.get_TotalEMISSIONS(partsid, 'wsv', peer)
    
    if wsv_value != offdb_value:
        print("Validation Failed")
    else :
        print("Validation Successful")
        

########################################################
## calculating TotalEmissions by recursive processing ##
########################################################

def calculate_totalemissions(partsid, peer):
    datalink = get_DataLink(partsid, peer)
    childpartsid = common.get_ChlidParts(partsid, peer)
    emissions = common.get_TotalEMISSIONS(partsid, 'wsv', datalink)   # child_totalEmissionの取得と合計
    
    if not childpartsid :
        common.IROHA_COMMANDexecutor(partsid, emissions, 0.0, 'admin@test', peer) # コマンドによる再計算
        return common.get_TotalEMISSIONS(partsid, 'wsv', datalink)

    else :
        data =  0
        for i in range(len(childpartsid)):
            data += calculate_totalemissions(childpartsid[i], get_DataLink(childpartsid[i], peer))
    
        common.IROHA_COMMANDexecutor(partsid, emissions, data, 'admin@test', peer) # コマンドによる再計算
        return data


###################################
## validation without WSV values ##
###################################

def original_validatioin(partsid, peer):
    offdb_value = common.get_TotalEMISSIONS(partsid, 'off', peer) # 比較元:offchainDB上の値
    calculate_totalemissions(partsid, peer)

    #validation
    wsv_value = common.get_TotalEMISSIONS(partsid, 'wsv', peer)
    
    if wsv_value != offdb_value:
        print("Validation Failed")
    else :
        print("Validation Successful")


if __name__ == '__main__':

    #quickly_calculate_totalemissions('P01001', get_DataLink('P01001', 'PeerA'))
    print(get_DataLink('P01001', 'PeerA'))
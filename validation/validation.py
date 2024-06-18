import common
import sys #コマンドライン変数


##############################################
## more quickly validation using WSV values ##
##############################################

def more_quickly_validation(partsid, peer):
    wsv_value = common.get_TotalEMISSIONS(partsid, peer, 'wsv') # Comparison destination : values in WSV
    offdb_value = common.get_TotalEMISSIONS(partsid, peer, 'off') # Comparison source : values in offchainDB

    if wsv_value != offdb_value:
        print("Validation Failed")
    else :
        print("Validation Successful")


########################################################
## quickly validation using child_parts in WSV values ##
########################################################

def quickly_validation(partsid, peer):
    offdb_value = common.get_TotalEMISSIONS(partsid, peer, 'off') # Comparison source : values in offchainDB

    # calculating child_totalEmission with WSV values
    child_partsid = common.get_ChlidParts(partsid, peer) # get child_partsids
    sum_child_emissions = 0
    for i in range(len(childpartsid)) : # get and sum  child_partsids
        sum_child_emissions += common.get_TotalEMISSIONS(i, peer, 'wsv') 
    
    # calculating TotalEmissions
    emissions = common.get_TotalEMISSIONS(partsid, peer, 'wsv') # get and sum child_totalEmission
    common.IROHA_COMMANDexecutor(partsid, emissions, sum_child_emissions, peer, 'admin@test') # recalculating with command

    #validation
    wsv_value = common.get_TotalEMISSIONS(partsid, peer, 'wsv')
    
    if wsv_value != offdb_value:
        print("Validation Failed")
    else :
        print("Validation Successful")
        

########################################################
## calculating TotalEmissions by recursive processing ##
########################################################

def calculate_totalemissions(partsid, peer):
    datalink = common.get_DataLink(partsid, peer)
    childpartsid = common.get_ChlidParts(partsid, peer)
    emissions = common.get_TotalEMISSIONS(partsid, datalink, 'wsv')   # get and sum child_totalEmission

    if not childpartsid :
        common.IROHA_COMMANDexecutor(partsid, emissions, '0.0', peer, 'admin@test') # recalculating with command
        return common.get_TotalEMISSIONS(partsid, datalink, 'wsv')

    else :
        data =  0
        for i in range(len(childpartsid)):
            data += calculate_totalemissions(childpartsid[i], common.get_DataLink(childpartsid[i], peer))
    
        common.IROHA_COMMANDexecutor(partsid, emissions, data, peer, 'admin@test') # recalculating with command
        return data


###################################
## validation without WSV values ##
###################################

def original_validatioin(partsid, peer):
    offdb_value = common.get_TotalEMISSIONS(partsid, peer, 'off') # Comparison source : values in offchainDB
    calculate_totalemissions(partsid, peer)

    #validation
    wsv_value = common.get_TotalEMISSIONS(partsid, peer, 'wsv')
    
    if wsv_value != offdb_value:
        print("Validation Failed")
    else :
        print("Validation Successful")


if __name__ == '__main__':

    #quickly_calculate_totalemissions('P01001', common.get_DataLink('P01001', 'A'))
    print(common.get_DataLink('P01001', 'A'))
import common

def original_calcu(partsid, peer, emissions):
    datalink = common.get_DataLink(partsid, peer)
    childpartsid = common.get_ChlidParts(partsid, peer)

    if not childpartsid :
        common.IROHA_COMMANDexecutor(partsid, emissions, '0.0', peer, 'admin@test') # recalculating with command
        return common.get_TotalEMISSIONS(partsid, datalink, 'wsv')

    else :
        data =  0
        for i in range(len(childpartsid)):
            data += calculate_totalemissions(childpartsid[i], common.get_DataLink(childpartsid[i], peer))
    
        common.IROHA_COMMANDexecutor(partsid, emissions, data, peer, 'admin@test') # recalculating with command
        return data

if __name__ == '__main__':

    original_calcu('P03007', 'postgresB', '1.0')
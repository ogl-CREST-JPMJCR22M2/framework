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

    ## B ##
    #original_calcu('P04016', 'postgresB', '1.2')
    #original_calcu('P04017', 'postgresB', '1.3')
    #original_calcu('P04023', 'postgresB', '1.0')
    #original_calcu('P04024', 'postgresB', '1.1')
    #original_calcu('P04030', 'postgresB', '1.2')
    #original_calcu('P03007', 'postgresB', '1.0')
    #original_calcu('P03009', 'postgresB', '1.1')

    ## C ##
    #original_calcu('P04014', 'postgresC', '1.0')
    #original_calcu('P04015', 'postgresC', '1.1')
    #original_calcu('P04018', 'postgresC', '1.0')
    #original_calcu('P04019', 'postgresC', '1.1')
    #original_calcu('P04020', 'postgresC', '1.0')
    #original_calcu('P04021', 'postgresC', '1.1')
    #original_calcu('P04022', 'postgresC', '1.2')
    #original_calcu('P04025', 'postgresC', '1.0')
    #original_calcu('P04026', 'postgresC', '1.1')
    #original_calcu('P04027', 'postgresC', '1.2')
    #original_calcu('P04028', 'postgresC', '1.0')
    #original_calcu('P04029', 'postgresC', '1.1')
    #original_calcu('P03006', 'postgresC', '1.1')
    #original_calcu('P03008', 'postgresC', '1.0')
    #original_calcu('P03012', 'postgresC', '1.2')

    ## B2 ##
    #original_calcu('P03013', 'postgresB', '1.3')

    ## A ##
    #original_calcu('P03005', 'postgresA', '1.0')
    #original_calcu('P03010', 'postgresA', '1.0')
    #original_calcu('P03011', 'postgresA', '1.1')
    #original_calcu('P02002', 'postgresA', '1.0')
    #original_calcu('P02003', 'postgresA', '1.1')
    #original_calcu('P02004', 'postgresA', '1.2')
    #original_calcu('P02001', 'postgresA', '1.0')
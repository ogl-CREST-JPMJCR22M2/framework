import commons as common
import time
    
def set_leafnode(partsid, peer):
    cfp = common.get_offchaindb_cfp(partsid, peer)
    datalink = get_DataLink(partsid, peer)
    common.update_data(partsid, cfp, datalink)
    common.update_wsv(partsid, cfp, datalink)

if __name__ == '__main__':

    #common.IROHA_COMMANDexecutor('P01001', 'SetAccountDetail','postgresA') 
    #common.IROHA_COMMANDexecutor('P02002', 'SetAccountDetail','postgresA')
    #common.IROHA_COMMANDexecutor('P02003', 'SetAccountDetail','postgresA')
    #common.IROHA_COMMANDexecutor('P02004', 'SetAccountDetail','postgresA')
    #common.IROHA_COMMANDexecutor('P03005', 'SetAccountDetail','postgresA')
    #common.IROHA_COMMANDexecutor('P03006', 'SetAccountDetail','postgresC')
    #set_leafnode('P03007','postgresB')
    #common.IROHA_COMMANDexecutor('P03008', 'SetAccountDetail','postgresC')
    #common.IROHA_COMMANDexecutor('P03009', 'SetAccountDetail','postgresB')
    #common.IROHA_COMMANDexecutor('P03010', 'SetAccountDetail','postgresA') 
    ##set_leafnode('P03010', 'postgresA')
    ##set_leafnode('P03011', 'postgresA')
    #common.IROHA_COMMANDexecutor('P03012', 'SetAccountDetail', 'postgresC')
    #common.IROHA_COMMANDexecutor('P03013', 'SetAccountDetail', 'postgresB')
    #set_leafnode('P04014', 'postgresC')
    #set_leafnode('P04015', 'postgresC')
    #set_leafnode('P04016', 'postgresB')
    #set_leafnode('P04017', 'postgresB')
    #set_leafnode('P04018', 'postgresC')
    #set_leafnode('P04019', 'postgresC')
    #set_leafnode('P04020', 'postgresC')
    #set_leafnode('P04021', 'postgresC')
    #set_leafnode('P04022', 'postgresC')
    #set_leafnode('P04023', 'postgresB')
    #set_leafnode('P04024', 'postgresB')
    #set_leafnode('P04025', 'postgresC')
    #set_leafnode('P04026', 'postgresC')
    #set_leafnode('P04027', 'postgresC')
    #set_leafnode('P04028', 'postgresC')
    #set_leafnode('P04029', 'postgresC')
    #set_leafnode('P04030', 'postgresB')

    start = time.time()

    for i in range(1, 3334):
        
        part_id = f'P{i:05d}'
        common.IROHA_COMMANDexecutor(part_id, 'SetAccountDetail','postgresA')
    
    t = time.time() - start
    print(t)

    
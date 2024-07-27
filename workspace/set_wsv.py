import commons as common
    
def set_leafnode(partsid, peer):
    cfp = common.get_offchaindb_cfp(partsid, peer)
    common.update_data(partsid, cfp, peer)

if __name__ == '__main__':

    common.IROHA_COMMANDexecutor('P01001', 'SetAccountDetail','postgresA') 
    common.IROHA_COMMANDexecutor('P02002', 'SetAccountDetail','postgresA')
    common.IROHA_COMMANDexecutor('P02003', 'SetAccountDetail','postgresA')
    common.IROHA_COMMANDexecutor('P02004', 'SetAccountDetail','postgresA')
    common.IROHA_COMMANDexecutor('P03005', 'SetAccountDetail','postgresA')
    common.IROHA_COMMANDexecutor('P03006', 'SetAccountDetail','postgresC')
    set_leafnode('P03007','postgresB')
    common.IROHA_COMMANDexecutor('P03008', 'SetAccountDetail','postgresC')
    common.IROHA_COMMANDexecutor('P03009', 'SetAccountDetail','postgresB')
    set_leafnode('P03010', 'postgresA')
    set_leafnode('P03011', 'postgresA')
    common.IROHA_COMMANDexecutor('P03012', 'postgresC', 'P02004')
    common.IROHA_COMMANDexecutor('P03013', 'postgresB', 'P02004')
    set_leafnode('P04014', 'postgresC')
    set_leafnode('P04015', 'postgresC')
    set_leafnode('P04016', 'postgresB')
    set_leafnode('P04017', 'postgresB')
    set_leafnode('P04018', 'postgresC')
    set_leafnode('P04019', 'postgresC')
    set_leafnode('P04020', 'postgresC')
    set_leafnode('P04021', 'postgresC')
    set_leafnode('P04022', 'postgresC')
    set_leafnode('P04023', 'postgresB')
    set_leafnode('P04024', 'postgresB')
    set_leafnode('P04025', 'postgresC')
    set_leafnode('P04026', 'postgresC')
    set_leafnode('P04027', 'postgresC')
    set_leafnode('P04028', 'postgresC')
    set_leafnode('P04029', 'postgresC')
    set_leafnode('P04030', 'postgresB')
    
from iroha import Iroha, IrohaCrypto, IrohaGrpc
import SQLexecutor as SQLexe

iroha = Iroha('admin@test')
priv_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'

###########################
## Get DataLink from wsv ##
###########################

def get_DataLink(partsid, peer):  #peer:executing peer

    SQL = sql.SQL("""
            SELECT DataLink FROM Partsinfo WHERE partsid = {PartsID};
        """).format(
            PartsID = sql.Literal(partsid)
        )
    return SQLexe.QUERYexecutor_wsv(SQL, peer)[0][0]


#############################
## Get cfp from offchainDB ##
#############################

def get_offchaindb_cfp(partsid, peer):  #peer:target peer

    SQL = sql.SQL("""
            SELECT cfp FROM offchaindb_cfpval WHERE partsid = {PartsID};
        """).format(
            PartsID = sql.Literal(partsid)
        )
    return str(SQLexe.QUERYexecutor_off(SQL, peer)[0][0])


###########################
## Get Totalcfp from wsv ##
###########################

def get_wsv_totalcfp(partsid, peer): #peer:target peer

    SQL = sql.SQL("""
            SELECT totalcfp FROM cfpval WHERE partsid = {PartsID};
        """).format(
            PartsID = sql.Literal(partsid)
        )
    return str(SQLexe.QUERYexecutor_wsv(SQL, peer)[0][0])


#######################
## UPDATE offchainDB ##
#######################

def update_data(partsid, totalcfp, peer):  #peer:target peer
    SQL = sql.SQL("""
            UPDATE offchaindb_cfpval set totalcfp = {totalcfp} 
            WHERE partsid = {PartsID} ;
        """).format(
            PartsID = sql.Literal(partsid),
            totalcfp = sql.Literal(totalcfp)
        )

    SQLexe.COMMANDexecutor_off(SQL, peer)


#######################
## Run iroha command ##
#######################

def IROHA_COMMANDexecutor(partsid, cmd, peer): #peer:executing peer
    
    if peer[8:] == 'A':
        net = IrohaGrpc('192.168.32.2:50051')
    elif peer[8:] == 'B':
        net = IrohaGrpc('192.168.32.3:50051')
    else :
        net = IrohaGrpc('192.168.32.4:50051')

    tx = iroha.transaction(
        [iroha.command(
            cmd,
            account_id = 'admin@test',
            parts_id = partsid
        )]
    )

    IrohaCrypto.sign_transaction(tx, priv_key)
    net.send_tx(tx)

    for status in net.tx_status_stream(tx):
        print(status)
    
    if status[0] == 'COMMITTED':
        totalcfp =  get_wsv_totalcfp(partsid, peer)
        datalink = get_DataLink(partsid, peer)
        update_data(partsid, totalcfp, datalink)
        return
    else:
        return
    

if __name__ == '__main__':

    partsid = 'P01001'
    #IROHA_COMMANDexecutor(partsid,'SetAccountDetail', 'postgresA')
    IROHA_COMMANDexecutor(partsid,'SubtractAssetQuantity', 'postgresA')
    
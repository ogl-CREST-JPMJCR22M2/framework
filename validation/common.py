from iroha import Iroha, IrohaCrypto, IrohaGrpc
from psycopg2 import sql
import SQLexecutor as SQLexe

iroha = Iroha('admin@test')
net = IrohaGrpc('localhost:50051')
priv_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'


############################
## Insert into offchainDB ##
############################

def insert_data(partsid, totalemissions, emissions, peer):
    SQL = sql.SQL("""
            INSERT INTO offchaindb_co2emissions (partsid, totalemissions, emissions) VALUES ({PartsID}, {TotalEMISSIONS}, {EMISSIONS})
            ON CONFLICT (partsid)
            DO UPDATE SET totalemissions = {TotalEMISSIONS}, emissions = {EMISSIONS};
        """).format(
            PartsID = sql.Literal(partsid),
            TotalEMISSIONS = sql.Literal(totalemissions),
            EMISSIONS = sql.Literal(emissions)
        )

    SQLexe.COMMANDexecutor(SQL, peer, 'off')


###############################################
## Get TotalEMISSIONS from offchainDB or WSV ##
###############################################

def get_TotalEMISSIONS(partsid, peer, db = 'off'):
    tablename = 'offchaindb_co2emissions'

    if db == 'wsv':
        tablename = 'co2emissions'

    SQL = sql.SQL("""
            SELECT totalemissions FROM {TABLEname} WHERE partsid = {PartsID};
        """).format(
            TABLEname = sql.Identifier(tablename),
            PartsID = sql.Literal(partsid)
        )

    return SQLexe.QUERYexecutor(SQL, peer, db)[0][0]


###################################
## Get EMISSIONS from offchainDB ##
###################################

def get_EMISSIONS(partsid, peer):

    SQL = sql.SQL("""
            SELECT emissions FROM offchaindb_co2emissions WHERE partsid = {PartsID};
        """).format(
            PartsID = sql.Literal(partsid)
        )
    return SQLexe.QUERYexecutor(SQL, peer, db)[0][0]


################################
## Get Child_Partsid from wsv ##
################################

def get_ChlidParts(partsid, peer): #peer:executing peer(account)

    SQL = sql.SQL("""
            SELECT childpartsid FROM Partsinfo WHERE partsid = {PartsID};
        """).format(
            PartsID = sql.Literal(partsid)
        )
    return SQLexe.QUERYexecutor(SQL, peer, 'wsv')[0][0]


###########################
## Get DataLink from wsv ##
###########################

def get_DataLink(partsid, peer):  #peer:executing peer(account)

    SQL = sql.SQL("""
            SELECT DataLink FROM Partsinfo WHERE partsid = {PartsID};
        """).format(
            PartsID = sql.Literal(partsid)
        )
    return SQLexe.QUERYexecutor(SQL, peer, 'wsv')[0][0]


#######################
## Run iroha command ##
#######################

def IROHA_COMMANDexecutor(partsid, emissions, sumchildemissions, peer, accountid = 'admin@test'):
    tx = iroha.transaction(
        [iroha.command(
            'SetAccountDetail',
                account_id = accountid,
                parts_id = partsid,
                new_emissions = emissions,
                sum_child_emissions = sumchildemissions
        )]
    )

    IrohaCrypto.sign_transaction(tx, priv_key)
    net.send_tx(tx)

    for status in net.tx_status_stream(tx):
        print(status)

    if status[0] == 'COMMITTED':
        totalemissions =  get_TotalEMISSIONS(partsid, peer, db = 'wsv')
        datalink = get_DataLink(partsid, peer)
        insert_data(partsid, totalemissions, emissions, datalink)
        return

    else:
        return


if __name__ == '__main__':

    partsid = 'n02001'
    totalemissions = 331.01
    emissions = '10001.0'
    sumchildemissions = '12345.0'

    #insert_data(partsid, totalemissions, emissions)
    #IROHA_COMMANDexecutor(partsid, emissions, sumchildemissions, 'admin@test')

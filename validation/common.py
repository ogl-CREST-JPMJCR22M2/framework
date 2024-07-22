from iroha import Iroha, IrohaCrypto, IrohaGrpc
from psycopg2 import sql
import SQLexecutor as SQLexe

iroha = Iroha('admin@test')
priv_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'


##########################################
## !NOT USE NOW! UPSERT into offchainDB ##
##########################################

def upsert_data(partsid, totalemissions, emissions, peer):
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


#######################
## UPDATE offchainDB ##
#######################

def update_data(partsid, totalemissions, emissions, peer):
    SQL = sql.SQL("""
            UPDATE offchaindb_co2emissions set totalemissions = {TotalEMISSIONS}, emissions = {EMISSIONS} 
            WHERE partsid = {PartsID} ;
        """).format(
            PartsID = sql.Literal(partsid),
            TotalEMISSIONS = sql.Literal(totalemissions),
            EMISSIONS = sql.Literal(emissions)
        )

    SQLexe.COMMANDexecutor(SQL, peer, 'off')


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
    

###############################################
## Get TotalEMISSIONS from offchainDB or WSV ##
###############################################

def get_TotalEMISSIONS(partsid, peer, db = 'wsv'): 
    tablename = 'co2emissions'

    if db == 'off':
        tablename = 'offchaindb_co2emissions'
        peer = get_DataLink(partsid, peer)

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

def get_EMISSIONS(partsid, peer): #peer:executing peer(account)

    SQL = sql.SQL("""
            SELECT emissions FROM offchaindb_co2emissions WHERE partsid = {PartsID};
        """).format(
            PartsID = sql.Literal(partsid)
        )
    datalink = get_DataLink(partsid, peer)
    return str(SQLexe.QUERYexecutor(SQL, datalink, 'off')[0][0])


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


#######################
## Run iroha command ##
#######################

def IROHA_COMMANDexecutor(partsid, emissions, sumchildemissions, peer, accountid = 'admin@test'): #peer:executing peer(account)
    
    if peer[8:] == 'A':
        net = IrohaGrpc('192.168.32.2:50051')
    elif peer[8:] == 'B':
        net = IrohaGrpc('192.168.32.3:50051')
    else :
        net = IrohaGrpc('192.168.32.4:50051')
    
    if sumchildemissions == '0.0':
        sumchildemissions = str(float(emissions)/2)
        emissions = str(float(emissions)/2)
        zeroflag = True
    else :
        zeroflag = False

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
        if not zeroflag:
            update_data(partsid, totalemissions, emissions, datalink)
        else :
            update_data(partsid, totalemissions, str(float(emissions)*2), datalink)
        return get_TotalEMISSIONS(partsid, datalink, 'wsv')
    else:
        return False


##############################################################
## calculating child_TotalEmissions by recursive processing ##
##############################################################

def calcu_child_totalemissions(partsid, peer):
    childpartsid = get_ChlidParts(partsid, peer)

    if not childpartsid :
        return '0.0'
    else :
        data =  0
        for i in range(len(childpartsid)):
            datalink = get_DataLink(childpartsid[i], peer)
            child_totalEmissions = calcu_child_totalemissions(childpartsid[i], datalink)
            emissions = get_EMISSIONS(childpartsid[i], datalink)

            data += IROHA_COMMANDexecutor(childpartsid[i], emissions, child_totalEmissions, datalink, 'admin@test') 
            
    return str(data)




if __name__ == '__main__':

    partsid = 'n02001'
    totalemissions = 331.01
    emissions = '10001.0'
    sumchildemissions = '12345.0'

    #update_data(partsid, totalemissions, emissions)
    #IROHA_COMMANDexecutor(partsid, emissions, sumchildemissions, 'admin@test')

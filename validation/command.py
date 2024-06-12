from iroha import Iroha, IrohaCrypto, IrohaGrpc
from psycopg2 import sql
import SQLexecutor as SQLexe
import SQL

iroha = Iroha('admin@test')
net = IrohaGrpc('localhost:50051')
priv_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'

def get_childparts(partsid):

    SQL = sql.SQL("""
            SELECT childpartsid FROM co2emissions WHERE partsid = {PartsID};
        """).format(
            PartsID = sql.Literal(partsid)
        )

    return SQLexe.QUERYexecutor(SQL, 'wsv')[0][0]


def IROHA_COMMANDexecutor(partsid, emissions, sumchildemissions, accountid = 'admin@test'):
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
        totalemissions =  SQL.get_TotalEMISSIONS(partsid, db = 'wsv')
        SQL.insert_data(partsid, totalemissions, emissions)
        return

    else:
        return


if __name__ == '__main__':

    partsid = 'n02001'
    totalemissions = 331.01
    emissions = '10001.0'
    sumchildemissions = '12345.0'

    #insert_data(partsid, totalemissions, emissions)
    IROHA_COMMANDexecutor(partsid, emissions, sumchildemissions, 'admin@test')

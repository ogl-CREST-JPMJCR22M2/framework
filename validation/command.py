from iroha import Iroha, IrohaCrypto, IrohaGrpc
import sys #コマンドライン変数
from psycopg2 import sql
import SQLexecutor as SQLexe

iroha = Iroha('admin@test')
net = IrohaGrpc('localhost:50051')
priv_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'

def get_childTotalEMISSIONS(partsid):
    
    SQL = sql.SQL("""
            SELECT childpartsid FROM co2emissions WHERE partsid = {PartsID};
        """).format(
            PartsID = sql.Literal(partsid)
        )

    childpartsid = SQLexe.QUERYexecutor(SQL, 'wsv')
    print(type(childpartsid))

def IROHA_COMMANDexecutor(partsid, emissions, accountid = 'admin@test'):
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


if __name__ == '__main__':

    partsid = 'e02003'
    totalemissions = 331.01
    emissions = 1.33

    #insert_data(partsid, totalemissions, emissions)
    
    print(get_childTotalEMISSIONS(partsid))

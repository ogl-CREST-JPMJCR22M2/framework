from iroha import Iroha, IrohaCrypto, IrohaGrpc
from psycopg2 import sql

iroha = Iroha('admin@test')
priv_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'

#######################
## Run iroha command ##
#######################

def IROHA_COMMANDexecutor(partsid, peer): #peer:executing peer(account)
    
    if peer[8:] == 'A':
        net = IrohaGrpc('192.168.32.2:50051')
    elif peer[8:] == 'B':
        net = IrohaGrpc('192.168.32.3:50051')
    else :
        net = IrohaGrpc('192.168.32.4:50051')

    tx = iroha.transaction(
        [iroha.command(
            'SetAccountDetail',
                account_id = 'admin@test',
                parts_id = partsid
        )]
    )

    IrohaCrypto.sign_transaction(tx, priv_key)
    net.send_tx(tx)

    for status in net.tx_status_stream(tx):
        print(status)

if __name__ == '__main__':

    partsid = 'P01001'
    IROHA_COMMANDexecutor(partsid, 'postgresA')
    
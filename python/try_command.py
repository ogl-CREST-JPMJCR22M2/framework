from iroha import Iroha, IrohaCrypto, IrohaGrpc

iroha = Iroha('admin@test')
net = IrohaGrpc('localhost:50051')

priv_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'
tx = iroha.transaction(
 [iroha.command(
     'SetAccountDetail',
        account_id = 'admin@test',
        parts_id = 'e01001',
        new_emissions = '89.0',
        sum_child_emissions = '12345.0'
 )]
)

IrohaCrypto.sign_transaction(tx, priv_key)
net.send_tx(tx)

for status in net.tx_status_stream(tx):
    print(status)

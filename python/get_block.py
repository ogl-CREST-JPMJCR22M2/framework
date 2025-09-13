from iroha import Iroha, IrohaCrypto, IrohaGrpc

net = IrohaGrpc('localhost:50051')

iroha = Iroha('admin@test')
priv_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'

query = iroha.query(
            'GetBlock',
            height = 3
         )

IrohaCrypto.sign_query(query, priv_key)

response = net.send_query(query)

print(response)
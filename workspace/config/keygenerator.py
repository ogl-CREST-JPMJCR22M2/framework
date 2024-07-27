from iroha import IrohaCrypto

private_key = IrohaCrypto.private_key()
public_key = IrohaCrypto.derive_public_key(private_key)

print('public  key:' + str(public_key))
print('private key:' + str(private_key))
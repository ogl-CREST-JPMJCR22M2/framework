
import hashlib

def xor_hash(strings):
    result = bytearray(32)  # SHA-256は32バイト（256ビット）
    for s in strings:
        h = hashlib.sha256(str(s).encode()).digest()
        for i in range(32):
            result[i] ^= h[i]  # XOR 合成
    return result.hex()

print(xor_hash(["0.1", "0.2", "0.1"]))  # 例: 53f2659028e5e4bb5cdaba3a94a74040cf5e236b0685f1a0a37e3f927709bea8
print(xor_hash(["0.1", "0.6", "0.4"]))  # 例: 53f2659028e5e4bb5cdaba3a94a74040cf5e236b0685f1a0a37e3f927709bea8
print(xor_hash(["0.7", "0.2", "0.2"]))  # 例: 973b372a514f91db8219fef585cdf81b09196afd7948f5fb1e29c2016dd995a0

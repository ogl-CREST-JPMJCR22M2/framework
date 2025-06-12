
import hashlib

def xor_hash(strings):
    result = bytearray(32)  # SHA-256は32バイト（256ビット）
    for s in strings:
        h = hashlib.sha256(str(s).encode()).digest()
        for i in range(32):
            result[i] ^= h[i]  # XOR 合成
    return result.hex()

print(xor_hash(["868fb7d14a1eda99855671497734a2c34a8e825170e7c4992b5459648b3d1ea4", "6b9a6e6ca589abb266e1c98cfb4bb69fec88f63c16a3b92b754af99477a04276"]))  # 例: 53f2659028e5e4bb5cdaba3a94a74040cf5e236b0685f1a0a37e3f927709bea8
print(xor_hash(["3.2472"]))  # 例: 53f2659028e5e4bb5cdaba3a94a74040cf5e236b0685f1a0a37e3f927709bea8
print(xor_hash(["ee19f019f803a4bdc3c46f0e6fe250cff1f7dd799f241c967b8d600028d16151", "5ecc781418e94a50428fc393824d71a338a604f8639e01761ad072bb53d0f53b"]))  # 例: 973b372a514f91db8219fef585cdf81b09196afd7948f5fb1e29c2016dd995a0

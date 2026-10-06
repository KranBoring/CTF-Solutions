from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def AESkeyOutput(lfsr):
    key = bytearray()
    for count in range(16):
        byte = ""
        for i in range(8):
            feedback = lfsr[63] ^ lfsr[61] ^ lfsr[60] ^ lfsr[58]
            pop = lsfr.pop(0) 
            byte += str(pop)
            lfsr.append(feedback)
        key += long_to_bytes(int(byte, 2))
    return bytes(key)
def AESkeyTap(lfsr):
    key = bytearray()
    for count in range(16):
        byte = ""
        for i in range(8):
            feedback = lfsr[63] ^ lfsr[61] ^ lfsr[60] ^ lfsr[58]
            pop = lsfr.pop(0)
            byte += str(feedback)
            lfsr.append(feedback)
        key += long_to_bytes(int(byte, 2))
    return bytes(key)

lsfr = [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1]

keyoutput = AESkeyOutput(lsfr)
keytap = AESkeyTap(lsfr)

ciphertext = bytes.fromhex("5fdec2e502a7c8d5951f41da4b0e0057fa1c4a5dcf3ecb8affd53e58f05cdfb138338e7e04fbddef0c6260a4eb758417")

cipheroutput = AES.new(keyoutput, AES.MODE_ECB)
ciphertap = AES.new(keytap, AES.MODE_ECB)
flag1 = cipheroutput.decrypt(ciphertext)
flag2 = ciphertap.decrypt(ciphertext)

try:
    print(unpad(flag1,AES.block_size))
except Exception:
    print(flag1)
try:
    print(unpad(flag2,AES.block_size))
except Exception:
    print(flag2)

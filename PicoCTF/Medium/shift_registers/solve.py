from Crypto.Util.number import *

with open("output.txt", "r") as f:
    cipher = bytes.fromhex(f.read())

def steplfsr(lfsr):
    b7 = (lfsr >> 7) & 1
    b5 = (lfsr >> 5) & 1
    b4 = (lfsr >> 4) & 1
    b3 = (lfsr >> 3) & 1

    feedback = b7 ^ b5 ^ b4 ^ b3
    lfsr = (feedback << 7) | (lfsr >> 1)
    return lfsr

def decrypt_lfsr(pt_bytes, key):
    output = bytearray()
    lfsr = key
    for p in pt_bytes:
        output.append(p ^ lfsr)
        lfsr = steplfsr(lfsr)
    return bytes(output)

format = b"a"
key = chr(format[0] ^ cipher[0]).encode()
flag = decrypt_lfsr(cipher, bytes_to_long(key))
print(flag.decode())

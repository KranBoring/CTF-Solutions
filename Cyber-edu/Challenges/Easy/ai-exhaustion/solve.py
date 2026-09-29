from Crypto.Util.number import *

B91_ALPHABET = [chr(i) for i in range(33, 124)]
def base91_decode(data):
    return bytes([B91_ALPHABET.index(data[i]) * len(B91_ALPHABET) + B91_ALPHABET.index(data[i+1]) for i in range(0,len(data),2)])
def affine_decrypt(data):
    a = 7
    b = 13
    inver_a = inverse(a, 256)
    return bytes([((x-13)*inver_a) % 256 for x in data])
def xor_layer(data: bytes, key: bytes) -> bytes:
    return bytes([c ^ key[i % len(key)] for i, c in enumerate(data)])
with open("cipher.txt","r") as f:
    enc = f.read()
xored = affine_decrypt(base91_decode(enc))
pt_head = xor_layer(b'175544', xored[:6]) 
AES_KEY = xor_layer((pt_head * 2)[:10], xored[:10])
flag = xor_layer(xored, AES_KEY).decode()
print(flag)
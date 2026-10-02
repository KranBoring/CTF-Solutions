from pwn import *

with open("output.txt","r") as f:
    cipher = bytes.fromhex(f.read().strip())

key = bytearray()
key.extend(xor(cipher[32:], b'\x3f' * 16))

format = b"TFCCTF{"
for i in range(len(format)):
    key[i] = cipher[i] ^ format[i]

print(xor(key, cipher))
from aes import *
import os

key_length = int(input("Choose key length (16, 24, 32): "))
key = os.urandom(key_length)
cipher = CustomAES(key)

while True:
    plaintext = bytes.fromhex(input(">>> "))
    if plaintext == b'guess':
        break
    assert len(plaintext) <= 32, "Too long!"
    enc = cipher.encrypt(plaintext, None)
    print(enc.hex())

input_key = bytes.fromhex(input('>>> '))
if input_key == key:
    print(open('flag.txt').read())
import requests
import itertools
from pwn import xor
import string

printable = set(string.printable.encode())

url = "https://aes.cryptohack.org/stream_consciousness/encrypt/"
s = requests.session()

ciphertext = set()
while len(ciphertext) < 23:
    ciphertext.add(s.get(url).json()["ciphertext"])
with open("ciphertext.txt",'w') as f:
    for cipher in ciphertext:
        f.write(f"{cipher}\n")

check = set()
for tup in itertools.combinations(ciphertext, 2):
    cipher1, cipher2 = bytes.fromhex(tup[0]), bytes.fromhex(tup[1])
    result = xor(xor(cipher1, cipher2), b'crypto{')
    if result[:7] == b'Perhaps' or result[:7] == b'Would I':
        if cipher1 in check:
            with open("ciphertext.txt",'a') as f:
                f.write(f"{tup[0]}\n")
        check.add(cipher1)
        check.add(cipher2)
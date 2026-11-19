#!/usr/bin/env python3
from itertools import product

random_strs = [
    b'my encryption method',
    b'is absolutely impenetrable',
    b'and you will never',
    b'ever',
    b'break it'
]

def encrypt(ptxt, key):
    ctxt = b''
    for i in range(len(ptxt)):
        a = ptxt[i]
        b = key[i % len(key)]
        ctxt += bytes([a ^ b])
    return ctxt

def main() -> None:
    with open("output.txt") as f:
        ciphertext = bytes.fromhex(f.read().strip())
    for mask in product([0, 1], repeat=5):
        copy = ciphertext
        for i in range(len(mask)):
            if mask[i] == 1:
                copy = encrypt(copy, random_strs[i])
        key_head = encrypt(copy[:8], b'picoCTF{')
        if all(32 <= b < 127 for b in key_head):
            print(mask, key_head, encrypt(bytes([copy[-1]]), b"}\n"))

    mask = (0, 0, 1, 1, 1)
    for i in range(len(mask)):
        if mask[i] == 1:
            ciphertext = encrypt(ciphertext, random_strs[i])
    flag = encrypt(ciphertext, b"Africa!")
    print(flag.decode())
    


if __name__ == "__main__":
    main()

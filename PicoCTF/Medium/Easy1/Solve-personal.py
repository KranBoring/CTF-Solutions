#!/usr/bin/env python3
from CTF_Crypto_Attack.Symmetric import vigenere_cipher

def main() -> None:
    key = "SOLVECRYPTO"
    ciphertext = "UFJKXQZQUNB"
    flag = vigenere_cipher(ciphertext, key, 'decode')
    print(flag)

if __name__ == "__main__":
    main()
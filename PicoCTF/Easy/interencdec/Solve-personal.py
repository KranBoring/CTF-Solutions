#!/usr/bin/env python3
from CTF_Crypto_Attack.Symmetric import caesar_cipher
from base64 import b64decode

def main() -> None:
    data = open("enc_flag").read()
    ciphertext = b64decode((b64decode(data).decode()).split('\'')[1]).decode()
    for key in range(26):
        flag = caesar_cipher(ciphertext, key, 'decode')
        if flag.startswith('academy'):
            print(flag)
            break

if __name__ == "__main__":
    main()
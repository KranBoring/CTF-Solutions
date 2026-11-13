#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import parsers
from decrypt import decrypt_flag

def main() -> None:
    data = parsers('output.txt')
    p, g, A, B, iv, ciphertext = data['p'], data['g'], data['A'], data['B'], data['iv'], data['encrypted_flag']
    b = B ^ g
    S = A ^ b % p
    flag = decrypt_flag(S, iv, ciphertext)
    print(flag)
if __name__ == "__main__":
    main()
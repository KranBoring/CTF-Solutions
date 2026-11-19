#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import parsers
from CTF_Crypto_Attack.RSA import factorize_n, decrypt

def main() -> None:
    n, c = parsers('output.txt', parse_hex_int=True).values()
    factors = factorize_n(n)
    flag = decrypt(ct=c,factors=factors,mode='cefs')
    print(flag)

if __name__ == "__main__":
    main()

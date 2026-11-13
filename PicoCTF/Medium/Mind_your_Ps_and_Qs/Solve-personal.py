#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import parsers, get_factors
from CTF_Crypto_Attack.RSA import decrypt


def main() -> None:
    data = parsers("values")
    n = data['n']
    e = data['e']
    c = data['c']
    p ,q = get_factors(n, prime_only_mode=True)
    flag = decrypt(c, e=e, factors=[q, p], advanced_mode=True)
    print(flag[::-1])
if __name__ == "__main__":
    main()
#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import parsers, get_factors
from CTF_Crypto_Attack.RSA import decrypt


def main() -> None:
    data = parsers("values")
    n = data['n']
    e = data['e']
    c = data['c']
    p ,q = get_factors(n, prime_only_mode=True)
    flag = decrypt(c, e=e, factors=[q, p], mode='cefs')
    print(flag[::-1])

from CTF_Crypto_Attack.Util import parsers
from CTF_Crypto_Attack.RSA import decrypt, factorize_n
from time import time
def main1() -> None:
    data = parsers("values")
    n = data['n']
    start = time()
    print(factorize_n(N=n))
    print(f"Thời gian chạy: {(time() - start):.2f}s")
if __name__ == "__main__":
    main()
    main1()
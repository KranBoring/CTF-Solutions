#!/usr/bin/env python3
from CTF_Crypto_Attack.RSA import cube_root
from CTF_Crypto_Attack.Util import parsers
def main() -> None:
    data = parsers("message.txt")
    N = data['n']
    e = data['e']
    ct = data['c']
    flag = cube_root(ct, N, e)
    print(flag)

if __name__ == "__main__":
    main()
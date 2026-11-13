#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import parsers
from CTF_Crypto_Attack.RSA import cube_root

FLAG = b"crypto{???????????????????????????????????}"

def main() -> None:
    data = parsers("output.txt")
    n, e, c = data.values()
    flag_len = len(FLAG)
    pad_len = 100 - flag_len
    inv_pad = pow(pow(2, -1, n), 24 * pad_len, n)
    c_new = (c * inv_pad) % n
    flag = cube_root(c_new, n)
    print(flag)
if __name__ == "__main__":
    main()
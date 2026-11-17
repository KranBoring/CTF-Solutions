#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import parsers
from CTF_Crypto_Attack.RSA import common_factor_gcd, decrypt_crt
from Crypto.Util.number import bytes_to_long, long_to_bytes

def main() -> None:
    n1, n2, n3, e, c = parsers("public-key.txt").values()
    factored = common_factor_gcd([n1, n2, n3])
    for n in [n3, n2, n1]:
        c = decrypt_crt(
            ct=c,
            factors=list(factored[n]),
            decode_mode=False
        )
        c = bytes_to_long(c)
    print(long_to_bytes(c).decode())
if __name__ == "__main__":
    main()

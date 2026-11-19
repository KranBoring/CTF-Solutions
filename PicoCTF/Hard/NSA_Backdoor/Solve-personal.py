#!/usr/bin/env python3
from sage.all import * 
from Crypto.Util.number import long_to_bytes
from CTF_Crypto_Attack.Util import parsers
from CTF_Crypto_Attack.RSA import factorize_n

def main() -> None:
    n ,c = parsers("output.txt", parse_hex_int=True).values()
    p, q = factorize_n(n)
    F_p = GF(p)
    F_q = GF(q)
    flag_p = F_p(c).log(3)
    flag_q = F_q(c).log(3)
    o_p = F_p(3).multiplicative_order()
    o_q = F_q(3).multiplicative_order()
    flag = crt([flag_p, flag_q], [o_p, o_q])
    print(long_to_bytes(flag).decode())
if __name__ == "__main__":
    main()

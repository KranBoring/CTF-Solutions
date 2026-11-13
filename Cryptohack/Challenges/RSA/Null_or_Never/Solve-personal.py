#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import parsers
from CTF_Crypto_Attack.RSA import coppersmith_stereotyped_message
from Crypto.Util.number import bytes_to_long

FLAG = b"crypto{???????????????????????????????????}"

def main() -> None:
    data = parsers("output.txt")
    n, e, c = data.values()
    
    flag_len = len(FLAG)
    pad_len = 100 - flag_len

    pre = b"crypto{"
    suf = b"}" + b"\x00" * pad_len

    unknown_len = flag_len - len(pre) - 1
    unknown_bits = unknown_len * 8
    suf_bits = len(suf) * 8

    a = 1 << suf_bits
    b = bytes_to_long(pre + b"\x00" * unknown_len + suf)
    flag = coppersmith_stereotyped_message(
        c=c,
        N=n,
        unknown_bits=unknown_bits,
        e=3,
        a=a,
        b=b
    )
    print(f"crypto{{{flag}}}")
if __name__ == "__main__":
    main()
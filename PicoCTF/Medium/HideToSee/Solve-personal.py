#!/usr/bin/env python3
from CTF_Crypto_Attack.Symmetric import atbash_cipher

def main() -> None:
    ct = "zxzwvnb{zgyzhs_xizxp_zz003u7z}"
    flag = atbash_cipher(ct)
    print(flag)
if __name__ == "__main__":
    main()
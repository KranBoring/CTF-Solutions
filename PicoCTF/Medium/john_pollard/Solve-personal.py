#!/usr/bin/env python3
from CTF_Crypto_Attack.RSA import decrypt, pollard_p_minus_1
from Crypto.PublicKey import RSA



def main() -> None:
    with open("cert") as f:
        data = RSA.importKey(f.read())
    N = data.n
    e = data.e
    print(pollard_p_minus_1(N))
    print(N)

if __name__ == "__main__":
    main()
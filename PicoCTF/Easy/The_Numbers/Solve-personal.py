#!/usr/bin/env python3
from CTF_Crypto_Attack.Symmetric import A1Z26

def main() -> None:
    flag = [16, 9, 3, 15, 3, 20, 6, "{", 20, 8, 5, 14, 21, 13, 2, 5, 18, 19, 3, 1, 19, 15, 14, "}"]
    print(A1Z26(flag, 'decode'))


if __name__ == "__main__":
    main()
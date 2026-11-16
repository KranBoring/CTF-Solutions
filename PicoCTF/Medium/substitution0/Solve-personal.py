#!/usr/bin/env python3
from CTF_Crypto_Attack.Symmetric import break_substitution_cipher

def main() -> None:
    message = open("message.txt").read()
    flag = break_substitution_cipher(
        ciphertext=message,
        restarts=26
    )
    print(flag[flag.index("academy{"):flag.index("}") + 1])

if __name__ == "__main__":
    main()

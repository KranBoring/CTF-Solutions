#!/usr/bin/env python3
import subprocess
from CTF_Crypto_Attack.Symmetric import caesar_cipher
def main() -> None:
    cmd = "cat leak/passwords.txt | grep \"{\""
    cipher = subprocess.check_output(cmd, shell=True, text=True)
    for key in range(26):
        flag = caesar_cipher(cipher, key, 'decode')
        if flag.startswith("academy"):
            print(flag)
            break

if __name__ == "__main__":
    main()
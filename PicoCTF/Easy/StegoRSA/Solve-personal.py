#!/usr/bin/env python3
import subprocess
from Crypto.PublicKey import RSA
from CTF_Crypto_Attack.RSA import decrypt
from Crypto.Util.number import bytes_to_long

def main() -> None:
    cmd = "exiftool image.jpg | grep \"Comment\""
    data = subprocess.check_output(cmd, shell=True, text=True).split(' ')[-1]
    key = RSA.importKey(bytes.fromhex(data).decode())
    with open("flag.enc", "rb") as f:
        flag = bytes_to_long(f.read())
    flag = decrypt(flag, key.d, key.n, decode_mode=False).split(b'\x00', 1)[-1].decode()
    print(flag)
if __name__ == "__main__":
    main()
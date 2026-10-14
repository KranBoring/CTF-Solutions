import json
import hashlib
import requests
from Crypto.Cipher import AES

url = "https://aes.cryptohack.org/passwords_as_keys/"
keys = [hashlib.md5(word.strip().encode()).digest() for word in open("words.txt").readlines()]
ciphertext = bytes.fromhex(json.loads(requests.get(f"{url}encrypt_flag/").text)["ciphertext"])

for key in keys:
    cipher = AES.new(key, AES.MODE_ECB)
    flag = cipher.decrypt(ciphertext)
    if flag.startswith(b"crypto{"):
        print(flag.decode())
        break
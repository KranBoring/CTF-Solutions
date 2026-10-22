import requests
import os
from Crypto.Util.Padding import unpad


s = requests.session()
url = "https://aes.cryptohack.org/triple_des/"

weak_key = "00"*8 + "ff"*8
ciphertext = s.get(f"{url}encrypt_flag/{weak_key}/").json()["ciphertext"]

flag = s.get(f"{url}encrypt/{weak_key}/{ciphertext}").json()["ciphertext"]

print(unpad(bytes.fromhex(flag), 8))

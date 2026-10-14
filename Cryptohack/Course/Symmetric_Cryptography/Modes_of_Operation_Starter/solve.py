import requests
import json

url = "https://aes.cryptohack.org/block_cipher_starter/"

ciphertext = json.loads(requests.get(f"{url}encrypt_flag/").text)["ciphertext"]
flag = bytes.fromhex(json.loads(requests.get(f"{url}decrypt/{ciphertext}/").text)["plaintext"]).decode("utf-8`")
print(flag)
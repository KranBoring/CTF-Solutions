import requests
from pwn import xor

s = requests.session()

url = "https://aes.cryptohack.org/lazy_cbc/"

payload = "aa" * 48
ciphertext = s.get(f"{url}encrypt/{payload}/").json()["ciphertext"]

payload = ciphertext[:32] + "00" * 16 + ciphertext[:32]
error = s.get(f"{url}receive/{payload}/").json()["error"].split(' ')[-1]

block1,block3 = bytes.fromhex(error[:32]),bytes.fromhex(error[64:])
key = xor(block1, block3)

payload = str(key.hex())
flag = bytes.fromhex(s.get(f"{url}get_flag/{payload}/").json()["plaintext"])

print(flag)
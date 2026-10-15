import requests
from pwn import *

url = "https://aes.cryptohack.org/ecbcbcwtf/"

s = requests.session()

ciphertext = s.get(f"{url}encrypt_flag/").json()["ciphertext"]
iv, ciphertext = bytes.fromhex(ciphertext[:32]),ciphertext[32:]

blocks = bytes.fromhex(s.get(f"{url}decrypt/{ciphertext}/").json()["plaintext"])
block1,block2 = blocks[:16],blocks[16:]

decblock1 = xor(iv, block1)
decblock2 = xor(bytes.fromhex(ciphertext[:32]),block2)

flag = decblock1 + decblock2

print(flag)


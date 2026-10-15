import requests
from pwn import xor

# Cach 1

url = "https://aes.cryptohack.org/symmetry/"
s = requests.session()

enc_flag = s.get(f"{url}encrypt_flag/").json()["ciphertext"]
iv, enc_flag = enc_flag[:32],bytes.fromhex(enc_flag[32:])

plaintext = len(enc_flag) * "00"
ciphertext = bytes.fromhex(s.get(f"{url}encrypt/{plaintext}/{iv}").json()["ciphertext"])

flag = xor(xor(enc_flag, ciphertext), bytes.fromhex(plaintext))

print(flag)

# Cach 2 (Nen su dung)

url = "https://aes.cryptohack.org/symmetry/"
s = requests.session()

enc_flag = s.get(f"{url}encrypt_flag/").json()["ciphertext"]
iv, enc_flag = enc_flag[:32],enc_flag[32:]

flag = bytes.fromhex(s.get(f"{url}encrypt/{enc_flag}/{iv}").json()["ciphertext"])

print(flag)
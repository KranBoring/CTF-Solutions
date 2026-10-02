from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt(ciphertext, timestamp):
    key = sha256(str(timestamp).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    flag = cipher.decrypt(ciphertext)
    return flag

timestamp = 1790147508
cipher = bytes.fromhex("1677f86f41155474ff5233bc79d0ec79ab610074d921fea1140a448f8c8329d9")

for i in range(timestamp - 10000, timestamp + 10000):
    flag = decrypt(cipher, i)
    if b"academy{" in flag:
        print(unpad(flag, AES.block_size))
        break

from Crypto.Cipher import AES
#from Crypto.Util.number import *

ct = bytes.fromhex("a58fd383d77105ed4cec2ff0eb3e483dea0d8bf2d963ce6e61a7c875a8b4edea")
for key in range(1000001):
    cipher = AES.new(key.to_bytes(16, "big"), AES.MODE_ECB)
    flag = cipher.decrypt(ct)
    if b"W1{" in flag:
        print(flag)

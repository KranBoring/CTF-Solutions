import numpy as np
from CTF_Crypto_Attack.SCA import SCA_second_order_AES
from Crypto.Cipher import AES

plaintexts = np.load("emanation/plaintexts.npy")
traces = np.load("emanation/traces.npy")

key = SCA_second_order_AES(plaintexts, traces, window_len=40, align_trigger=True, debug=True)

cipher = AES.new(key, AES.MODE_CTR, nonce=b"")
ciphertext = bytes.fromhex(open("emanation/sealed_order.hex").read())
flag = cipher.decrypt(ciphertext)
print(flag.decode())


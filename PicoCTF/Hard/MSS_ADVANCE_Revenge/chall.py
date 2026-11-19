from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib
import random

flag = b"academy{REDACTED}"

p = getPrime(1024)
def eval_poly(x, coeffs):
	total = 0
	for i in range(len(coeffs)):
		total *= x
		total += coeffs[i]
	return total % p

MASTER_KEY = hashlib.sha256(flag).digest()
coeffs = [bytes_to_long(MASTER_KEY)]
for i in range(29):
	co = hashlib.sha256(long_to_bytes(coeffs[-1])).digest()
	coeffs.append(bytes_to_long(co))

pairs = []
for i in range(20):
	x = random.randint(0,p)
	y = eval_poly(x, coeffs)
	pairs.append((x,y))

def encrypt_flag(flag):
	iv = b"\x00"*16
	cipher = AES.new(MASTER_KEY, AES.MODE_CBC, iv)
	enc = cipher.encrypt(pad(flag, 16))
	return iv.hex(), enc.hex()

enc_flag = encrypt_flag(flag)

print(f"{p = }")
print(f"{pairs = }")
print(f"{enc_flag = }")

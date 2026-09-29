import secrets
import random
import math
from Crypto.Util.number import isPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

FLAG = b"OSC{~}"
E = 0x10001

primes = []
for i in range(3, 8):
    seed = secrets.randbelow(2**i)
    rng = random.Random(seed)
    while True:
        p = rng._randbelow(1 << 256) | 1
        if isPrime(p):
            break
    primes.append(p)

N = math.prod(primes)

aes_key = secrets.token_bytes(16)
iv = secrets.token_bytes(16)
cipher = AES.new(aes_key, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(FLAG, AES.block_size))

aes_int = int.from_bytes(aes_key, 'big')
C_key = pow(aes_int, E, N)

with open('output.txt', 'w') as f:
    f.write(f"{hex(N)[2:]} {hex(C_key)[2:]} {iv.hex()} {ct.hex()}\n")

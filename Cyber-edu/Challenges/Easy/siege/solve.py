import random
import math
import collections
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import *

with open("output.txt","r") as f:
    data = f.read().split(' ')
N = int(data[0], 16)
C_key = int(data[1],16)
iv = bytes.fromhex(data[2])
ct = bytes.fromhex(data[3])
E = 65537

primes = []
Totient = []
N_cp = N
for i in range(3, 8):
    for seed in range(2**i):
        rng = random.Random(seed)
        while True:
            p = rng._randbelow(1 << 256) | 1
            if isPrime(p):
                break
        if N_cp % p != 0:
            continue
        else:
            N_cp //= p 
        primes.append(p)
        Totient.append(p-1)
count = collections.Counter(Totient)
T = math.prod((p+1)**(k-1)*p for p, k in count.items())
D = pow(E, -1, T)
aes_int = pow(C_key, D, N)
aes_key = aes_int.to_bytes(length=16, byteorder='big')
cipher = AES.new(aes_key,AES.MODE_CBC,iv)
flag = cipher.decrypt(ct)
flag = unpad(flag, AES.block_size)
print(flag)
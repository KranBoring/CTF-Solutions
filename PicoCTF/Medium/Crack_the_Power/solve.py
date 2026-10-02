import gmpy2
from Crypto.Util.number import *

with open("message.txt","r") as f:
    n = int(f.readline().strip().split(' ')[-1])
    e = int(f.readline().strip().split(' ')[-1])
    c = int(f.readline().strip().split(' ')[-1])
k = 0
while True:
    flag, ok = gmpy2.iroot(c + k * n, e)
    if b"academy{" in long_to_bytes(flag):
        print(long_to_bytes(flag).decode())
        print("k = ",k)
        break
    
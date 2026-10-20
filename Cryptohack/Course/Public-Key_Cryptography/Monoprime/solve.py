from Crypto.Util.number import *

with open("output.txt") as f:
    n = int(f.readline().strip().split(' ')[-1])
    e = int(f.readline().strip().split(' ')[-1])
    ct = int(f.readline().strip().split(' ')[-1])
T = n - 1
d = pow(e, -1, T)
flag = pow(ct, d, n)
print(long_to_bytes(flag))
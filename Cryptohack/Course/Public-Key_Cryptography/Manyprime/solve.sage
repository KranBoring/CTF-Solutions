from Crypto.Util.number import *
import time

with open("output.txt") as f:
    n = int(f.readline().strip().split(' ')[-1])
    e = int(f.readline().strip().split(' ')[-1])
    ct = int(f.readline().strip().split(' ')[-1])

start = time.time()
T = prod([i - 1 for i in ecm.factor(n)])
end = time.time()
print(f"ecm factor trong {end - start} giay")

d = pow(e, -1, T)
flag = pow(ct, d, n)
print(long_to_bytes(flag))

start = time.time()
T = prod([i[0] - 1 for i in factor(n)])
end = time.time()
print(f"factor trong {end - start} giay")

d = pow(e, -1, T)
flag = pow(ct, d, n)
print(long_to_bytes(flag))
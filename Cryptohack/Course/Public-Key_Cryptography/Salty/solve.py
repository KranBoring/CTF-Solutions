from Crypto.Util.number import *

with open("output.txt") as f:
    n = int(f.readline().strip().split(' ')[-1])
    e = int(f.readline().strip().split(' ')[-1])
    ct = int(f.readline().strip().split(' ')[-1])

print(long_to_bytes(ct))
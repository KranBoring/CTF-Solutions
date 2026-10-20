from Crypto.Util.number import long_to_bytes
import gmpy2

with open("output.txt") as f:
    n = int(f.readline().strip().split(' ')[-1])
    e = int(f.readline().strip().split(' ')[-1])
    ct = int(f.readline().strip().split(' ')[-1])

flag,ok = gmpy2.iroot(ct, e)
if ok:
    print(long_to_bytes(flag))
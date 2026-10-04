from Crypto.Util.number import *
import gmpy2
with open("values") as f:
    N = int(f.readline().strip())
    e = int(f.readline().strip())
    c = int(f.readline().strip())
k = 0
while True:
    flag, ok = gmpy2.iroot(c + N * k, e)
    if ok:
        flag = long_to_bytes(flag)
        if b"academy{" in flag:
            print(flag)
            break
        
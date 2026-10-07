from sage.all import *
from Crypto.Util.number import *

with open("output.txt") as f:
    x = int(f.readline().strip().split(' ')[-1],16)
    n = int(f.readline().strip().split(' ')[-1],16)
    c = int(f.readline().strip().split(' ')[-1],16)
e = 65537

R.<y> = PolynomialRing(ZZ)

P = y^2 - x * y + n 
q,p = P.roots(multiplicities=False)
T = (q - 1) * (p - 1)
d = pow(e, -1, T)
flag = pow(c, d, n)
print(long_to_bytes(flag))
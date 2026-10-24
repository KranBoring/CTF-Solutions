from sage.all import *
from Crypto.Util.number import *

def wiener(n ,e):
    n = ZZ(n)
    e = ZZ(e)
    conv = continued_fraction(e / n)
    R.<x> = PolynomialRing(ZZ)
    for phanso in conv.convergents():
        k = phanso.numerator()
        d = phanso.denominator()

        if k == 0 or (e * d - 1) % k != 0:
            continue

        t = (e * d - 1) // k 
        s = n - t + 1

        P = x^2 - s * x + n 
        roots = P.roots(multiplicities = False)
        if len(roots) == 2:
            return d 

with open("output.txt") as f:
    n = int(f.readline().strip().split(' ')[-1], 16)
    e = int(f.readline().strip().split(' ')[-1], 16)
    c = int(f.readline().strip().split(' ')[-1], 16)
d = wiener(n, e)
print(long_to_bytes(pow(c, d, n)))
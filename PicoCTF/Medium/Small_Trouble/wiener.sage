from sage.all import *
from Crypto.Util.number import *

with open("message.txt","r") as f:
    n = int(f.readline().split(' ')[2])
    e = int(f.readline().split(' ')[2])
    cipher = int(f.readline().split(' ')[2])
def wiener(N ,e):
    e = ZZ(e)
    N = ZZ(N)
    cf = continued_fraction(e / N)
    R.<x> = PolynomialRing(ZZ)
    for conv in cf.convergents():
        k = conv.numerator()
        d = conv.denominator()

        if k == 0 or (e * d - 1) % k != 0:
            continue

        T = (e * d - 1) // k
        s = N - T + 1

        P = x^2 - s * x + N 
        roots = P.roots(multiplicities=False)

        if len(roots) == 2:
            q , p = roots
            return d
d = wiener(n , e)
flag = pow(cipher, d, n)
print(long_to_bytes(flag))
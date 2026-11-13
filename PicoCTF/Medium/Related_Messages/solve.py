from sage.all import *
from Crypto.Util.number import *


with open("output.txt","r") as f:
    c1 = int(f.readline())
    c2 = int(f.readline())
    m1_m2 = int(f.readline())
    N = int(f.readline())
e = 17

def rgcd(f1, f2):
    while f2:
        f1, f2 = f2, f1 % f2    
    return f1.monic()


R.<x> = PolynomialRing(Zmod(N))
m1 = (x + m1_m2)^e - c1
m2 = (x)^e - c2
c_gcd = rgcd(m1 ,m2)
m2 = -c_gcd[0]
m1 = (m2 -m1_m2) 
print(long_to_bytes(int(m1)))
print(long_to_bytes(int(m2)))

from Crypto.Util.number import *
from sage.all import *

with open("public-key.txt") as f:
    n1 = int(f.readline().strip().split(' ')[-1])
    n2 = int(f.readline().strip().split(' ')[-1])
    n3 = int(f.readline().strip().split(' ')[-1])
    e = int(f.readline().strip().split(' ')[-1])
    c = int(f.readline().strip().split(' ')[-1])

p = GCD(n1, n2) 
q = n1 // p
r = n2 // p

for a, b, n in [(q, r, n3), (p, r, n2), (p, q, n1)]:
    d = pow(e, -1, (a-1)*(b-1))
    c = pow(c, d, n)

print(long_to_bytes(c))
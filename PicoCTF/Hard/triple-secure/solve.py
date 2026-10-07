from Crypto.Util.number import *
from sage.all import *

with open("public-key.txt") as f:
    n1 = int(f.readline().strip().split(' ')[-1])
    n2 = int(f.readline().strip().split(' ')[-1])
    n3 = int(f.readline().strip().split(' ')[-1])
    e = int(f.readline().strip().split(' ')[-1])
    c = int(f.readline().strip().split(' ')[-1])

p = GCD(n1, n2)
q = GCD(n1, n3)
r = GCD(n2, n3)
N = [n3, n2, n1]

T = []
T.append((q - 1) * (r - 1))
T.append((p - 1) * (r - 1))
T.append((p - 1) * (q - 1))

D = []
for t in T:
    D.append(pow(e, -1, t))

for d,n in zip(D,N):
    c = pow(c, d, n)
print(long_to_bytes(c))
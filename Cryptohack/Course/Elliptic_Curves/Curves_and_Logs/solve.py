from sage.all import *
from hashlib import sha1

E = EllipticCurve(GF(9739), [497, 1768])
Q_A = E(815, 3190)
n_B = 1829
S = Q_A * n_B
x = S.xy()[0]
hash = sha1(str(x).encode()).hexdigest()
print(f"crypto{{{hash}}}")

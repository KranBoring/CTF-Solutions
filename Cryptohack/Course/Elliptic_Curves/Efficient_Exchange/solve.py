from decrypt import decrypt_flag
from sage.all import *
data = {'iv': 'cd9da9f1c60925922377ea952afc212c', 'encrypted_flag': 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'}
x_QA = 4726
n_B = 6534
p = 9739
a = 497
b = 1768

vp = (pow(x_QA, 3, p) + a * x_QA + b) % p
y_QA = pow(int(vp), (p + 1) // 4, p)
E = EllipticCurve(GF(p), [a, b])
Q_A = E(x_QA, y_QA)
S = Q_A * n_B
shared_secret = int(S[0])
flag = decrypt_flag(shared_secret, data['iv'], data['encrypted_flag'])
print(flag)
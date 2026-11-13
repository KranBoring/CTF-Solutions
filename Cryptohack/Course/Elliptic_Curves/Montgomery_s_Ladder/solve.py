from sage.all import *

p = 2**255 - 19
F = GF(p)
A = F(486662)
B = F(1)

Gx = F(9)
rhs = Gx**3 + A * Gx**2 + Gx
Gy = rhs.sqrt()
G = (Gx, Gy)

def montgomery_add(P, Q):
  if P is None:
    return Q
  if Q is None:
    return P
  x1, y1 = P
  x2, y2 = Q
  if x1 == x2:
    if y1 == -y2:
      return None
    return montgomery_double(P)

  alpha = (y2 - y1) / (x2 - x1)
  x3 = B * alpha**2 - A - x1 - x2
  y3 = alpha * (x1 - x3) - y1
  return (x3, y3)

def montgomery_double(P):
  if P is None:
    return None
  x1, y1 = P
  if y1 == 0:
    return None

  alpha = (3 * x1**2 + 2 * A * x1 + 1) / (2 * B * y1)
  x3 = B * alpha**2 - A - 2 * x1
  y3 = alpha * (x1 - x3) - y1
  return (x3, y3)

def montgomery_ladder(P, k: int):
  R0 = P
  R1 = montgomery_double(P)

  # Duyệt từ bit thứ hai (n - 2) về bit 0
  for bit in bin(k)[3:]:
    if bit == "0":
      R0, R1 = montgomery_double(R0), montgomery_add(R0, R1)
    else:
      R0, R1 = montgomery_add(R0, R1), montgomery_double(R1)
  return R0

k = 0x1337C0DECAFE
Q = montgomery_ladder(G, k)
print(f"crypto{{{int(Q[0])}}}")
#---------------------------------
from sage.all import *

p = (2**255) - 19
F = GF(p)
E = EllipticCurve(F, [0,486662,0,1,0])

G_x = F(9)
G = E.lift_x(G_x)
k = 0x1337c0decafe
Q = k*G

print(f"crypto{{{Q.xy()[0]}}}")
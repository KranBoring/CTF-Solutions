from sage.all import *

F = GF(9739)
E = EllipticCurve(F, [497, 1768])

P = E(493, 5564)
Q = E(1539, 4742)
R = E(4403, 5202)
S = P + P + Q + R
print(f"crypto{{{S[0]},{S[1]}}}")
#------------------------------------#
class Elliptic:
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self. b = b

    def __call__(self, x, y):
        return Point(self, x, y)

class Point:
    def __init__(self, curve, x, y):
        self.curve = curve
        self.x = x
        self.y = y

    def values(self):
        return (self.x, self.y)

    def __add__(self, point):
        p = self.curve.p
        a = self.curve.a

        if (self.x, self.y) == (0, 0):
            return point
        elif (point.x, point.y) == (0, 0):
            return self

        if (self.x == point.x) and (self.y + point.y) % p == 0:
            return Point(self.curve, 0, 0)
        else:
            if self.values() != point.values():
                lamda = ((point.y - self.y) * pow(point.x - self.x, -1, p)) % p
            else:
                lamda = ((3 * self.x**2 + a) * pow(2 * self.y, -1, p)) % p
        x = (lamda**2 - self.x - point.x) % p
        y = (lamda*(self.x - x) - self.y) % p
        return Point(self.curve, x, y)

E = Elliptic(9739, 497, 1768)
P = E(493, 5564)
Q = E(1539, 4742)
R = E(4403, 5202)
S = P + P + Q + R
x, y = S.values()
print(f"crypto{{{x},{y}}}")

        
        



import sys
import types

from Crypto.Random import get_random_bytes, random
from Crypto.Util.number import getPrime

sys.modules["turtle"] = types.ModuleType("turtle")
sys.path.insert(0, "/opt/dragon-crypto")

import dragon
from koblitz import koblitz_encoder


class HeadlessTurtle:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.heading = 0

    def penup(self): pass
    def pendown(self): pass
    def pencolor(self, _): pass

    def goto(self, x, y):
        self.x, self.y = x, y

    def left(self, angle):
        self.heading += angle

    def right(self, angle):
        self.heading -= angle

    def forward(self, distance):
        heading = self.heading % 360
        if heading == 0:
            self.x += distance
        elif heading == 90:
            self.y += distance
        elif heading == 180:
            self.x -= distance
        else:
            self.y -= distance

    def xcor(self): return self.x
    def ycor(self): return self.y


dragon.ob = HeadlessTurtle()
flag = open("flag.txt").read().strip()

while True:
    p = getPrime(256, randfunc=get_random_bytes)
    if p % 4 != 3:
        continue

    a = random.randrange(1 << 255, p)
    b = random.randrange(1 << 255, p)
    if (4 * pow(a, 3, p) + 27 * pow(b, 2, p)) % p == 0:
        continue

    points = koblitz_encoder(flag, a, b, p)
    if len(points) == len(flag):
        break

private_key = (
    random.randrange(1 << 127, 1 << 128),
    random.randrange(10, 15),
    random.randrange(2) * 180,
    a,
    b,
)

encrypted = [dragon.dragon_render(point, private_key) for point in points]
print(dragon.point_to_character(encrypted))

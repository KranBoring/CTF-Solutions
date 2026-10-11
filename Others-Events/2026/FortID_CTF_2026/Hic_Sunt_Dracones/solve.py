import dragon
from koblitz import koblitz_decoder
with open("output.txt") as f:
    data = f.read()

points = dragon.character_to_point(data)
flag = ""
for j in range(1,20):
    noise = points[-1][0] - (ord("}") * 20 + j)
    for point in points:
        if point[0] > 3000:
            x_new = point[0] - noise
        elif point[0] < -3000:
            x_new = point[0] + noise
        else:
            x_new = point[0]
        flag += koblitz_decoder([(x_new, point[1])])
    print(flag)
    flag = ""

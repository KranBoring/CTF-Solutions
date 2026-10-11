import math
from random import randint
#import matplotlib.pyplot as plt


def sq_root_mod_n(n, p):
    n %= p
    y = pow(n, (p + 1) // 4, p)
    return y if y * y % p == n else 0


def koblitz_encoder(plainText, elliptic_a, elliptic_b, p):
    ord_lst = [ord(ch) for ch in plainText]
    k = 20

    x_coords = []
    y_coords = []
    encoded_points = []

    for m in ord_lst:
        for j in range(1, k):
            x_m = m*k+j
            n = pow(x_m, 3) + elliptic_a * x_m + elliptic_b
            y_m = sq_root_mod_n(n, p)
            if (y_m != 0):
                x_coords.append(x_m)
                y_coords.append(y_m)
                encoded_points.append((x_m, y_m))
                break

    encoded = []
    for i in range(len(x_coords)):
        encoded.append((x_coords[i], y_coords[i]))
        #print('{},{}'.format(x_coords[i], y_coords[i]))
    return encoded


def koblitz_decoder(encoded_points):
    decoded_Msg = []
    k = 20
    for x, y in encoded_points:
        d = math.floor((x-1)/k)
        decoded_Msg.append(chr(d))

    # print(''.join(decoded_Msg))
    return ''.join(decoded_Msg)

# plt.plot(x_coords,y_coords,'s')
# plt.show()


'''
if __name__ == "__main__":
    plainText = input("Enter Message: ")

    print('Curve Parameters')
    elliptic_a = int(input("Enter A: "))
    elliptic_b = int(input("Enter B: "))

    encrypt = koblitz_encoder(plainText, elliptic_a, elliptic_b)

    print("Encrypted points: ", encrypt)

    decrypt = koblitz_decoder(encrypt)
    #decrypt = koblitz_decoder([(1856,292)])

    print("Decrypted message: ", decrypt)
'''
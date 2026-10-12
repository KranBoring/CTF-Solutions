from Crypto.Util.number import *
import gmpy2

def CrackingRSA(n,e,c):
    k = 0
    while True:
        root, ok = gmpy2.iroot(c + k * n, e)
        k += 1
        if ok:
            return long_to_bytes(root)
def readfile(file):
    n = int(file.readline().strip().split(' ')[2])
    e = int(file.readline().strip().split(' ')[2])
    c = int(file.readline().strip().split(' ')[2])
    return n,e,c
with open("output.txt") as f:
    flag = ""
    for i in range(7):
        n,e,c = readfile(f)
        flag += CrackingRSA(n,e,c)
print(flag)
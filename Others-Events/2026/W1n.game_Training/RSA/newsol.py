from Crypto.Util.number import *
import gmpy2
from sage.all import *

def readfile(file):
    n = int(file.readline().strip().split(' ')[2])
    e = int(file.readline().strip().split(' ')[2])
    c = int(file.readline().strip().split(' ')[2])
    return (n,e,c)
list_so = []
with open("output.txt") as f:
    for i in range(7):
        list_so.append(readfile(f))
list_mod = []
list_cipher = []
for i in list_so:
    list_mod.append(i[0])
    list_cipher.append(i[2])
M = crt(list_cipher, list_mod)
m, ok = gmpy2.iroot(M, 3)
print(long_to_bytes(m))
from Crypto.Util.number import *
import gmpy2
from sage.all import *
import itertools

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

lenght = list(range(7))
for c in itertools.combinations(lenght, 3):
    l_m = [list_mod[i] for i in c]
    l_c = [list_cipher[i] for i in c]
    M = crt(l_c, l_m)
    m, ok = gmpy2.iroot(M, 3)
    if ok:
        print(long_to_bytes(m).decode())
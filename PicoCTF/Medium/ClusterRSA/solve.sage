from sage.all import *
import math
from Crypto.Util.number import *

with open("message.txt","r") as f:
    n = int(f.readline().strip().split(' ')[-1])
    e = int(f.readline().strip().split(' ')[-1])
    ct = int(f.readline().strip().split(' ')[-1])
list_factor = [9671406556917033397931773,9671406556917033398314601,9671406556917033398439721,9671406556917033398454847]
T = math.prod([i-1 for i in list_factor])
d = pow(e, -1, T)
flag = pow(ct, d, n)
print(long_to_bytes(flag))
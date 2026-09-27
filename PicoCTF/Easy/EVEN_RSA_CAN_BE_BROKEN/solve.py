from pwn import *
from Crypto.Util.number import *

io = remote("chatelaine.cylabacademy.net", 28763)

N = int(((io.recvline()).decode()).split(' ',1)[1])
e = int(((io.recvline()).decode()).split(' ',1)[1])
cipher = int(((io.recvline()).decode()).split(' ',1)[1])

q,p = 2, N//2
T = (q-1)*(p-1)
d = pow(e,-1,T)
flag = long_to_bytes(pow(cipher,d,N))
print(flag)
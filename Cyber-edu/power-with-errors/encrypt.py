from Crypto.Util.number import *
import secrets
def xor(A,B):
  return bytes([a^^b for (a,b) in zip(A,B)])

p=getPrime(128)
n=10
t=5
c=3
F=open("params","w")
F.write(f"{p=}\n{n=}\n{t=}\n{c=}")
F.close()
flag=open("flag.txt",'rb').read()
assert(len(flag)<=n*n)
flag+=b"\x00"*(n*n-len(flag))
for T in range(t):
  A=random_matrix(GF(p),n,n)
  out=[]
  for _ in range(c):
    key=b"\x00"+os.urandom(n*n-1)
    print(list(key))
    flag=xor(key,flag)
    U=pow(A,secrets.randbelow(p)).list()
    U=[a+b for (a,b) in zip(U,key)]
    out.append(U)
  F=open(f"testcase_{T}.in","w")
  F.write(f"{out}")
  F.close()

F=open(f"enc","wb")
F.write(flag)
F.close()

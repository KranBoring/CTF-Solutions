from pwn import *
from json import dumps
from Crypto.Util.number import getPrime

host = "localhost"
port = 13385
io = remote(host, port)

def json(prime, base):
    return dumps({"prime":prime, "base":base}).encode()

if __name__ == "__main__":
    res = io.recvline()
    p,q = getPrime(425), getPrime(425)
    io.sendline(json(p * q, 113))
    res = io.recvline()
    print(res)
from pwn import *
from decrypt import decrypt_flag
import json
from sage.all import *

host = "socket.cryptohack.org"
port = 13379

io = remote(host, port)

def reuntil(text):
    res = io.recvuntil(text.encode())
    print(res.decode())

def payload(payload):
    io.sendline(payload)
    print(payload)

def reline():
    res = io.recvline()
    print(res)
    return json.loads(res.strip().decode())

reuntil("}")
payload("{\"supported\": [\"DH64\"]}".encode())

reuntil("}")
payload("{\"chosen\": \"DH64\"}".encode())

reuntil("Intercepted from Alice: ")
data = reline()
p = int(data["p"],16)
g = int(data["g"],16)
A = int(data["A"],16)

reuntil("Intercepted from Bob: ")
data = reline()
B = int(data["B"],16)

reuntil("Intercepted from Alice: ")
data = reline()
iv = data["iv"]
ciphertext = data["encrypted_flag"]

F = GF(p)
a = discrete_log(F(A), F(g))
shared_secret = pow(B, a, p)
flag = decrypt_flag(shared_secret, iv, ciphertext)
print(flag)
from pwn import *
from decrypt import decrypt_flag
import json

host = "socket.cryptohack.org"
port = 13371

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
    return res

reuntil("Intercepted from Alice: ")
data = reline()

reuntil("Send to Bob: ")
payload(data)

pay = json.dumps({"B": "01"}).encode()
reuntil("Send to Alice:")
payload(pay)

reuntil("Intercepted from Alice: ")
data = json.loads(reline().strip().decode())

iv = data["iv"]
ciphertext = data["encrypted_flag"]
flag = decrypt_flag(1,iv,ciphertext)

print(flag)






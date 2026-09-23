from pwn import *

io = remote("titan.picoctf.net", 54583)

response = io.recvuntil("decrypt.")
print(response.decode())
io.send(b"E\n")

response = io.recvuntil("keysize): ")
print(response.decode())
payload = b'\x02' + b'\n'
io.send(payload)

response = io.recvuntil("ciphertext (m ^ e mod n) ")
print(response.decode())
enc2 = io.recvline()

num = int(enc2.decode()) * 1765037049764047724348114634473658734830490852066061345686916365658618194981097216750929421734812911680434647401939068526285652985802740837961814227312100

response = io.recvuntil("decrypt.")
print(response.decode())
payload = b'D' + b'\n'
io.send(payload)

response = io.recvuntil('decrypt:')
print(response.decode())
payload = str(num).encode() + b'\n'
io.send(payload)

response = io.recvuntil("(c ^ d mod n): ")
print(response.decode())
dec = io.recvline()
print(dec.decode())
num = int(dec.decode(),16)//2
print(num)
print(hex(num))

hex_string = hex(num)[2:]
byte_array = bytes.fromhex(hex_string)
print(byte_array.decode('ascii'))



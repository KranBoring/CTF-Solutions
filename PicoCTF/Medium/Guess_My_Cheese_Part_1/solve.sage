from sage.all import *
from pwn import *

io = remote("xebec.cylabacademy.net",17001)

def payload(payload):
    io.sendline(str(payload).encode())
def reuntil(m):
    response = io.recvuntil(m.encode())
    print(response.decode())
def n(M):
    return ord(M) - ord('A')

reuntil("Here's my secret cheese -- if you're Squeexy, you'll be able to guess it:  ")
ciphertext = io.recvline().decode().strip()
print(ciphertext)
# Lấy cheese mã hóa
reuntil("What would you like to do?")
payload("e")
print("e")
reuntil("What cheese would you like to encrypt? ")
payload("cheddar")
print("cheddar")
reuntil("Here's your encrypted cheese:  ")
cheesecipher = io.recvline().decode().strip()
print(cheesecipher)
# Lấy kết quả của phép mã hóa để bắt đầu giải hệ phương trình tuyến tính tìm ra hệ số a,b
A = matrix(Zmod(26),[
    [n('C'),1],
    [n('H'),1]
])
B = vector(Zmod(26),[n(cheesecipher[0]), n(cheesecipher[1])])
C = A.solve_right(B)
sol_C = [int(i) for i in C]
cheese = ""
for i in ciphertext:
    cheese += chr(((n(i) - sol_C[1]) * pow(sol_C[0], -1, 26)) % 26 + ord('A'))
reuntil("What would you like to do?")
payload('g')
print("g")
reuntil("So...what's my cheese?")
payload(cheese)
print(cheese)
io.interactive()
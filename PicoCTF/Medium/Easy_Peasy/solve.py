from pwn import *

io = remote("chatelaine.cylabacademy.net", 37937)
target_cipher = "9de54e34304f7fb09a725d7afd5115fe8cc435178b3ebf96f9bc5b9bf7df3d86"
list_cipher = [int(i) for i in bytes.fromhex(target_cipher)]
def payload(payload):
    io.sendline(str(payload).encode())
    print(payload)
def reuntil(text):
    res = io.recvuntil(text.encode())
    print(res.decode())


reuntil("What data would you like to encrypt?")
payload("0" * 50000)
reuntil("Here ya go!\n")
answer = io.readline().strip().decode()
answer = [int(i) for i in bytes.fromhex(answer[100000-64:100000])]
key = []
flag = ""
for i in range(len(list_cipher)):
    key.append(ord('0') ^ answer[i])
    flag += chr(key[i] ^ list_cipher[i])
print("academy{"+flag+"}")
io.interactive()



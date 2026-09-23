from pwn import * 

io = remote("wily-courier.picoctf.net", 58281)
flag = ""
try:
    while True:
        word_int = io.recvline()
        flag += chr(int(word_int.decode()))
except EOFError:
    print(flag)
    io.close()

from pwn import *
from collections import Counter

host = "training.hkcert26.pwnable.hk"
port = 28109
io = remote(host, port)

payload = b"e\n" * 10000
io.send(payload)
res = io.clean(timeout=2)
ciphertext = [ct[2:] for ct in res.splitlines()[3:-1]]
password = ""
for i in range(16):
    char = [cipher[i] for cipher in ciphertext]
    counter = Counter(char)
    most = counter.most_common(1)[0][0]
    password += chr(most)
io.send(b'g\n')
io.clean(timeout=2)
io.send(password.encode() + b'\n')
flag = io.clean(timeout=2)
io.close()
print(flag.decode())


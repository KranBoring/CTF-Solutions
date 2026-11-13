from pwn import *

class Challenge:
    def __init__(self):
        self.r = remote('training.hkcert26.pwnable.hk', 20028)
    
    def send(self, m):
        self.r.sendlineafter(b'[cmd] ', f'send {format(m, "x")}')
        return int(self.r.recvline().strip().decode(), 16)

    def pkey(self):
        self.r.sendlineafter(b'[cmd] ', 'pkey')
    
    def backup(self):
        self.r.sendlineafter(b'[cmd] ', 'backup')
        return int(self.r.recvline().strip().decode(), 16)

    def flag(self):
        self.r.sendlineafter(b'[cmd] ', f'flag')
        return bytes.fromhex(self.r.recvline().decode())
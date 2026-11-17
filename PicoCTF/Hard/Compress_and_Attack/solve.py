#!/usr/bin/env python3
from CTF_Crypto_Attack.Symmetric import compression_oracle
from CTF_Crypto_Attack.Util import BaseSocketOracle
from pwn import remote
import string

io = remote("chatelaine.cylabacademy.net", 19794)

class Oracle(BaseSocketOracle):
    def get_length(self, plaintext):
        self.io.recvuntil(b":")
        self.io.sendline(plaintext)
        self.io.recvline()
        self.io.recvline()
        return int(self.io.recvline().strip().decode())
    def get_lengths_batch(self, pts):
        self.pipeline_send(pts, format_func=lambda v: v)
        length_list = []
        for _ in range(len(pts)):
            self.io.recvuntil(b": ")
            self.io.recvline()
            self.io.recvline()
            length_list.append(int(self.io.recvline().strip().decode()))
        return length_list
         

def main() -> None:
    oracle = Oracle(io)
    flag = compression_oracle(
        oracle=oracle,
        known_prefix=b"academy{",
        charset=(string.ascii_letters + "_{}").encode(),
        max_workers=1,
        debug=True
    )
    print(flag)
if __name__ == "__main__":
    main()

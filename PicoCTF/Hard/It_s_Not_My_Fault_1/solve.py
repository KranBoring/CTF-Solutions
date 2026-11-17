#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import BaseSocketOracle, parsers
from Crypto.Util.number import GCD
from hashlib import md5
from pwn import remote

io = remote("xebec.cylabacademy.net", 36752)

class Oracle(BaseSocketOracle):
    def bypass_first_round(self):
        res = self.io.recv().strip().decode()
        number_str = res.split('"')[1]
        hex_digits = res.split(':')[-1][1:]
        i = 0
        while md5((number_str + str(i)).encode()).hexdigest()[-6:] != hex_digits:
            i += 1
        self.io.sendline((number_str + str(i)).encode())

def main() -> None:
    oracle = Oracle(io)
    oracle.bypass_first_round()
    N, e = parsers(oracle.io.clean(timeout=2).strip().decode()).values()
    base = pow(2, e, N)
    cur = base
    for _ in range(1, (1 << 20) + 1):
        p = GCD(cur - 2, N)
        if p != 1:
            q = N // p
            break
        cur = (cur * base) % N
    oracle.io.sendline(str(q + p).encode())
    print(oracle.io.recvall(timeout=2).decode())
if __name__ == "__main__":
    main()

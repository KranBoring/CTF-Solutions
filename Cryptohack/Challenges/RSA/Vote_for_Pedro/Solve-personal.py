#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import BaseSocketOracle
from Crypto.Util.number import bytes_to_long, long_to_bytes
from sage.all import *
from pwn import remote

vote = bytes_to_long(b'\x00VOTE FOR PEDRO')

def json(vote):
    return {'option':'vote', 'vote':vote}

io = remote("socket.cryptohack.org", 13375)

def main() -> None:
    N_new = 2**120
    R = Zmod(N_new)
    payload = R(vote).nth_root(3)
    oracle = BaseSocketOracle(io)
    oracle.clear_banner()
    flag = oracle.send_json(json(vote=long_to_bytes(int(payload)).hex()))['flag']
    print(flag)

if __name__ == "__main__":
    main()

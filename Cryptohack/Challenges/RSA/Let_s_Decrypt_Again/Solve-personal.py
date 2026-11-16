#!/usr/bin/env python3
from CTF_Crypto_Attack.DH_DLP import craft_smooth_dh_params
from CTF_Crypto_Attack.Util import BaseSocketOracle
from Crypto.Util.number import long_to_bytes, bytes_to_long
from pkcs1 import emsa_pkcs1_v15
from sage.all import *
from pwn import remote, xor

io = remote("socket.cryptohack.org", 13394)

class Oracle(BaseSocketOracle):
    def get_signature(self):
        N, e, self.sig = map(lambda v: int(v, 16), self.send_json({'option':'get_signature'}).values())
    def set_pubkey(self, N):
        status, self.suffix = self.send_json({'option':'set_pubkey','pubkey':long_to_bytes(N).hex()}).values()
        self.weak_N = N
    def solve(self, msg, index):
        msg = msg + self.suffix
        digest = bytes_to_long(emsa_pkcs1_v15.encode(msg.encode(), 96))
        R = Zmod(self.weak_N)
        e = long_to_bytes(int(R(digest).log(R(self.sig)))).hex()
        return bytes.fromhex(self.send_json({'option':'claim','msg':msg, 'e':e,'index':index})['secret'])

def main() -> None:
    q = craft_smooth_dh_params(400)[0]
    weak_N = q**2
    oracle = Oracle(io)
    oracle.clear_banner()
    oracle.get_signature()
    oracle.set_pubkey(weak_N)
    tasks = [
        ("This is a test for a fake signature.", 0),
        ("My name is skibidi and I own CryptoHack.org", 1),
        ("Please send all my money to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", 2)
    ]
    secrets = [oracle.solve(msg, idx) for msg, idx in tasks]
    flag = xor(secrets[0], xor(secrets[1], secrets[2])).decode()
    print(flag)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import BaseSocketOracle
from Crypto.Util.number import bytes_to_long
from pwn import remote
from pkcs1 import emsa_pkcs1_v15

io = remote("socket.cryptohack.org", 13391)

class Oracle(BaseSocketOracle):
    def json_form(self, op=None, msg=None, N=None, e=None):
        if op == 'get_signature':
            return {'option':'get_signature'}
        else:
            return {'option':'verify','N':hex(N),'e':hex(e),'msg':msg}


def main() -> None:
    oracle = Oracle(io)
    oracle.clear_banner()
    N, e, sig = oracle.send_json(oracle.json_form(op="get_signature")).values()
    msg = "I am Mallory and I own CryptoHack.org"
    payload = emsa_pkcs1_v15.encode(msg.encode(), 256)
    N_payload = int(sig, 16) - bytes_to_long(payload)
    e_payload = 1
    flag = next(iter(oracle.send_json(oracle.json_form(msg=msg, N=N_payload, e=e_payload)).values()))
    print(flag)

if __name__ == "__main__":
    main()

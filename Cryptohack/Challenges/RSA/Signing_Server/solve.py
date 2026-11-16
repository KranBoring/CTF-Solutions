#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import BaseSocketOracle, magical_decode
from pwn import remote

class Oracle(BaseSocketOracle):
    def json(self, op=None, msg = None):
        return {
            "option":"get_secret"
        } if op == "get_secret" else {
            "option":"sign","msg":msg
        }

io = remote("socket.cryptohack.org", 13374)

def main() -> None:
    oracle = Oracle(io)
    oracle.clear_banner()
    secret = next(iter(oracle.send_json(oracle.json(op="get_secret")).values()))
    flag_hex = next(iter(oracle.send_json(oracle.json(msg=secret)).values()))
    flag = magical_decode(flag_hex[2:])
    print(flag)
if __name__ == "__main__":
    main()
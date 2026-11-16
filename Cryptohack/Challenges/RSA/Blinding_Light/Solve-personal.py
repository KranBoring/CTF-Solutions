#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import BaseSocketOracle
from Crypto.Util.number import bytes_to_long
from pwn import remote

ADMIN_TOKEN = b"admin=True"

class Oracle(BaseSocketOracle):
    def json_format(self, op=None, msg=None, sig=None):
        if op == 'get_pubkey':
            return {'option':op}
        if op == 'sign':
            return {'option':op, 'msg':msg}
        if op == 'verify':
            return {'option':op, 'msg':msg, 'signature':sig}

io = remote("socket.cryptohack.org", 13376)

def main() -> None:
    oracle = Oracle(io)
    oracle.clear_banner()
    N, e = oracle.send_json(oracle.json_format(op='get_pubkey')).values()
    N, e = int(N, 16), int(e, 16)
    payload_number = f"{2:02x}"
    payload_admin_token = f"{((bytes_to_long(ADMIN_TOKEN) * 2) % N):02x}"
    two = int(oracle.send_json(oracle.json_format(op='sign',msg=payload_number))['signature'], 16)
    two_mul_admin_token = int(oracle.send_json(oracle.json_format(op='sign',msg=payload_admin_token))['signature'], 16)
    val = (two_mul_admin_token * pow(two, -1, N)) % N
    sign_admin_token = f"{val:02x}"
    flag = oracle.send_json(oracle.json_format(op='verify',msg=f"{bytes_to_long(ADMIN_TOKEN):02x}",sig=sign_admin_token))['response']
    print(flag)

if __name__ == "__main__":
    main()

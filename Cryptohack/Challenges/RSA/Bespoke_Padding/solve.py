from pwn import *
from CTF_Crypto_Attack.Util import BaseSocketOracle
from CTF_Crypto_Attack.RSA import franklin_reiter_related_message

io = remote("socket.cryptohack.org", 13386)

class Oracle(BaseSocketOracle):
    def json(self):
        return {"option":"get_flag"}

def main():
    oracle = Oracle(io)
    io.recvline()
    ciphers = []
    for _ in range(2):
        output = oracle.send_json(oracle.json())
        json = {'c':output['encrypted_flag'],'N':output['modulus'],'a':output['padding'][0],'b':output['padding'][1]}
        ciphers.append(json)
    cipher1, cipher2 = ciphers
    c1, N, a1, b1 = cipher1.values()
    c2, N, a2, b2 = cipher2.values()
    flag = franklin_reiter_related_message(c1, c2, N, 11, a1, b1, a2, b2)
    print(flag)
if __name__ == '__main__':
    main()
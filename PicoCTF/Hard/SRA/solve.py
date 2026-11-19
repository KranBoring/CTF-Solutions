from pwn import remote
from sympy import EX
from CTF_Crypto_Attack.Util import BaseSocketOracle, parsers
from CTF_Crypto_Attack.RSA import decrypt
from sage.all import divisors, is_prime, Integer
from itertools import combinations

io = remote("xebec.cylabacademy.net", 18154)

class Oracle(BaseSocketOracle):
    def get_c_d(self):
        return parsers(self.io.recvline().strip().decode() + '\n' + self.io.recvline().strip().decode()).values()
    def send_pride(self, m):
        self.io.recvuntil(b"> ")
        self.io.sendline(m.encode())
        print(self.io.recvall().strip().decode())
        
def check(a):
    return (is_prime(a) and 127 < Integer(a).log(2) < 128)

def main():
    oracle = Oracle(io)
    c, d = oracle.get_c_d()
    e = 0x10001
    primes = []
    for a_minus in divisors(e*d - 1):
        a = a_minus + 1
        if check(a):
            primes.append(a)
    for q, p in combinations(primes, 2):
        try:
            msg = decrypt(c, d, p * q)
        except Exception:
            msg = None
        if msg:
            print(msg)
            break
    oracle.send_pride(msg)
if __name__ == '__main__':
    main()
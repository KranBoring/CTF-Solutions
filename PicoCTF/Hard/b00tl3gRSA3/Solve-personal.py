from Crypto.Util.number import *
from CTF_Crypto_Attack.RSA import factorize_n, decrypt
from CTF_Crypto_Attack.Util import parsers
from pwn import remote

def main():
    io = remote("xebec.cylabacademy.net", 38896)
    data = io.recvall()
    c, n ,e = parsers(data.decode()).values()
    factors = factorize_n(n)
    flag = decrypt(c, factors=factors, mode='cefs')
    print(flag)
if __name__ == '__main__':
    main()
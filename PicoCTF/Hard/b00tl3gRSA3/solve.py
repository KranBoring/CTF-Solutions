from CTF_Crypto_Attack.RSA import decrypt
from CTF_Crypto_Attack.Util import parsers
from pwn import remote
from sage.all import factor

def main():
    io = remote("xebec.cylabacademy.net", 38896)
    data = io.recvall()
    c, n ,e = parsers(data.decode()).values()
    factors = [factor for factor, _ in list(factor(n))]
    flag = decrypt(c, factors=factors, mode='cefs')
    print(flag)
if __name__ == '__main__':
    main()
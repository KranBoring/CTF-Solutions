from CTF_Crypto_Attack.Util import parsers
from CTF_Crypto_Attack.RSA import decrypt
from sage.all import *
def main():
    x, n, c = parsers("output.txt", parse_hex_int=True).values()
    R = PolynomialRing(ZZ, name='y')
    y = R.gen()
    P = y**2 - x * y + n 
    q,p = P.roots(multiplicities=False)
    flag = decrypt(ct=c, factors=[q, p], mode='cefs')
    print(flag)

if __name__ == '__main__':
    main()
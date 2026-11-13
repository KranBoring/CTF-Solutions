from CTF_Crypto_Attack.RSA import rsa_roots_crt
from CTF_Crypto_Attack.Util import parsers
def main():
    data = parsers("broken_rsa.txt")
    plaintext = rsa_roots_crt(data['ct'],data['e'],[data['n']])
    for plain in plaintext:
        if isinstance(plain, str):
            print(plain)
if __name__ == '__main__':
    main()
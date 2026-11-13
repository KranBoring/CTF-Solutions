from CTF_Crypto_Attack.Util import *
from CTF_Crypto_Attack.RSA import decrypt
def main():
    data = parsers.parsers("message.txt")
    primes = factordb.get_factors(data['n'], prime_only_mode=True)
    ct = data['ct']
    flag = decrypt(ct, factors=primes, advanced_mode=True)
    print(flag)

if __name__ == '__main__':
    main()
from sage.all import *
from Crypto.Util.number import long_to_bytes
from CTF_Crypto_Attack.Util.factordb import get_factors
from CTF_Crypto_Attack.RSA import decrypt_crt, decrypt

c = 2027792127378145444099302510462900300257442068928010403052259994880511317607407514908720534902489134379904618947792557805368190009359079320337075768626232418980864987406619809977532904702783433112202254001367719098893178820312980355187703995660867067442830169498602243151057835147454968516377852012013934653
e = 0x10001
m1 = 2**1024 - 3
m2 = 2**1022 - 2
m3 = 2**1020 - 1
m4 = 2**1018

factors = get_factors(m1, prime_only_mode=True)
for k0 in range(5):
    for k1 in range(5):
        for k2 in range(5):
            ciphertext = c + k0 * m4 + k1 * m3 + k2 * m2
            flag = decrypt_crt(ciphertext, e, factors)
            if flag is None:
                continue
            print(flag)
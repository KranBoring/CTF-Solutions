from itertools import combinations
from math import gcd
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes
from CTF_Crypto_Attack.RSA import phi_factors
ns = []
es = []
ciphers = []
for i in range(1, 51):
    ciphers.append(int(open(f"keys_and_messages/{i}.ciphertext").read(), 16))
    key = RSA.importKey(open(f"keys_and_messages/{i}.pem").read())
    ns.append(key.n)
    es.append(key.e)
for i in combinations(ns, 2):
    if i[0] == i[1]:
        continue
    p = gcd(i[0], i[1])
    if p > 1:
        assert i[0] % p == 0 
        q = i[0]// p
        break
N = p * q
T = phi_factors([q, p])
e = es[20]
ciphertext = ciphers[20]
d = pow(e, -1, T)
key = RSA.construct((N, e, d))
cipher = PKCS1_OAEP.new(key)
flag = cipher.decrypt(long_to_bytes(ciphertext)).decode()
print(flag)

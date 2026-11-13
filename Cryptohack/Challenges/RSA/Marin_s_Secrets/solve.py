from CTF_Crypto_Attack.Util.parsers import parsers
from CTF_Crypto_Attack.RSA import decrypt, phi_factors
#from math import log2

data = parsers('output.txt')
n = data['n']
e = data['e']
c = data['c']

#print(log2(n)/2)
q, p = 2**2203 - 1, 2**2281 - 1
T = phi_factors([q, p])
d = pow(e, -1, T)
flag = decrypt(c, d, n)
print(flag)
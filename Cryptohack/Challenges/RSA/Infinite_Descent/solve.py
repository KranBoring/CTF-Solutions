from CTF_Crypto_Attack.Util.parsers import parsers
from CTF_Crypto_Attack.RSA import fermat_factors, decrypt, phi_factors

data = parsers('output.txt')
n = data['n']
e = data['e']
c = data['c']
'''
def fermat(n):
    from math import isqrt
    a = isqrt(n)
    check = n - a * a
    b = isqrt(check)
    while b * b != check:
        a = a + 1
        check = a * a - n
        b = isqrt(check)
    p = a + b
    q = a - b
    return p, q
'''
q, p = fermat_factors(n)
T = phi_factors([q, p])
d = pow(e, -1, T)
flag = decrypt(c, d, n)
print(flag)
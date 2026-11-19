from math import log2

from CTF_Crypto_Attack.Util import parse_asn1_der

def main():
    key = parse_asn1_der("private.key")
    version, n, e, d, p, q, dP, dQ, qInv = key
    print(log2(n))
    print(log2(p))
    assert n % p == 0
    
if __name__ == '__main__':
    main()
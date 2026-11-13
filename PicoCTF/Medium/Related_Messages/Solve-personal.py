from sage.all import *
from CTF_Crypto_Attack.RSA import franklin_reiter_related_message


def main():
    with open("output.txt","r") as f:
        c1 = int(f.readline())
        c2 = int(f.readline())
        m1_m2 = int(f.readline())
        N = int(f.readline())
    e = 17

    m1, m2 = franklin_reiter_related_message(c1, c2, m1_m2, N , e, decode_mode=False)
    print(f"{m1}\n{m2}")
if __name__ == '__main__':
    main()
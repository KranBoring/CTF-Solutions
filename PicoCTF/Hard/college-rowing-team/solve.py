from CTF_Crypto_Attack.Util import parsers
from CTF_Crypto_Attack.RSA import cube_root
from itertools import combinations

def main():
    data = parsers("encrypted-messages.txt", multi_value=True)
    ns = data['n']
    e = 3
    cs = data['c']
    for i in range(len(ns)):
        print(cube_root(cs[i],ns[i]))
if __name__ == '__main__':
    main()
    


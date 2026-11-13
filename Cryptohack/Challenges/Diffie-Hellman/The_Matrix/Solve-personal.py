#!/usr/bin/env python3
from sage.all import *

def load_matrix(fname):
    data = open(fname, 'r').read().strip()
    rows = [list(map(int, row)) for row in data.splitlines()]
    return Matrix(GF(2), rows)

def binary_to_bytes(matrix):
    bits = ''.join([str(c) for col in matrix.columns() for c in col])
    bin_str = ''.join(bits)
    s = ''.join([chr(int(bin_str[i:i + 8], 2)) for i in range(0, len(bin_str), 8)])
    return s
def main() -> None:
    E = 31337
    ciphertext = load_matrix('flag.enc')
    ord_cipher = ciphertext.multiplicative_order()
    inv_E = pow(E, -1, int(ord_cipher))
    ciphertext = ciphertext**inv_E
    flag = binary_to_bytes(ciphertext)
    print(flag[:flag.index("}") + 1])

if __name__ == "__main__":
    main()
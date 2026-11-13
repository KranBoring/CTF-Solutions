#!/usr/bin/env python3
from sage.all import *
from json import loads
P = 13322168333598193507807385110954579994440518298037390249219367653433362879385570348589112466639563190026187881314341273227495066439490025867330585397455471
N = 30
def load_matrix(fname):
    data = open(fname, 'r').read().strip()
    rows = [list(map(int, row.split(' '))) for row in data.splitlines()]
    return Matrix(GF(P), rows)

def main() -> None:
    G = load_matrix("generator.txt")
    v, w = loads(open("output.txt").read()).values()
    v = vector(GF(P), v)
    w = vector(GF(P), w)
    
    print(v)
    print(w)
if __name__ == "__main__":
    main()
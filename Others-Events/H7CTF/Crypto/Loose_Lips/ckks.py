#!/usr/bin/env python3
# minimal CKKS-style approximate homomorphic encryption used by the analytics
# service. shipped so the scheme is known: ring R_q = Z_q[x]/(x^N+1), encoding by
# the canonical embedding at the primitive 2N-th roots of unity. the flaw is not in
# this code; it is that the service returns the approximate (noisy) decryption.
import numpy as np, secrets

N = 8
Q = (1 << 40) - 87           # prime modulus # 1.099.511.627.689
DELTA = 1 << 25              # scale # 33554432

_pows = [2 * k + 1 for k in range(N)] # [1, 3, 5, 7, 9, 11, 13, 15]
_roots = np.array([np.exp(1j * np.pi * p / N) for p in _pows])
_V = np.array([[r ** k for k in range(N)] for r in _roots])
_Vinv = np.linalg.inv(_V)

def _center(poly):
    return np.array([((c + Q // 2) % Q) - Q // 2 for c in poly], dtype=complex)

def decode(poly):
    """int poly -> complex slot vector (length N/2), scaled down by DELTA."""
    return list((_V @ _center(poly))[:N // 2] / DELTA)

def encode(z):
    """complex slot vector (length N/2) -> integer plaintext poly (length N)."""
    z = np.array(z, dtype=complex)
    full = np.concatenate([z, np.conj(z[::-1])]) * DELTA
    return [int(round(c.real)) % Q for c in (_Vinv @ full)]

def ring_mul(a, b):
    res = [0] * (2 * N)
    for i in range(N):
        if a[i]:
            for j in range(N):
                res[i + j] = (res[i + j] + a[i] * b[j]) % Q
    return [(res[i] - res[i + N]) % Q for i in range(N)]

def ring_add(a, b): return [(x + y) % Q for x, y in zip(a, b)]
def ring_sub(a, b): return [(x - y) % Q for x, y in zip(a, b)]

def small(bound=1):
    return [secrets.randbelow(2 * bound + 1) - bound for _ in range(N)]

def rand_poly():
    return [secrets.randbelow(Q) for _ in range(N)]

def keygen():
    return small(1)                                  # ternary secret key

def encrypt(values, s):
    """encrypt a length-(N/2) real/complex vector under secret key s -> (b, a)."""
    m = encode(values)
    a = rand_poly()
    e = small(3)
    b = ring_add(ring_sub([0] * N, ring_mul(a, s)), ring_add(m, e))   # b = -a*s + m + e
    return b, a

def decrypt(ct, s, smudge=0):
    """return the APPROXIMATE decryption (decoded slots). b + a*s = m + e."""
    b, a = ct
    d = ring_add(b, ring_mul(a, s))
    if smudge:
        d = ring_add(d, small(smudge))
    return decode(d)

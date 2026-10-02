#!/usr/bin/env python3


import itertools
import json
import math
import os
import random
import secrets
import sys

PARAMETERS = dict(p=17, n=32, m=34, t=16, s=4)

FLAG = os.environ.get("FLAG", "CSSCTF{REDACTED}")

def add(a, b, p, scale=1):
    out = dict(a)
    for mon, coefficient in b.items():
        value = (out.get(mon, 0) + scale * coefficient) % p
        if value:
            out[mon] = value
        else:
            out.pop(mon, None)
    return out


def mul(a, b, p):
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            mon = tuple(sorted(ma + mb))
            out[mon] = (out.get(mon, 0) + ca * cb) % p
    return {mon: c for mon, c in out.items() if c}


def substitute(poly, values, p):
    out = {}
    for mon, coefficient in poly.items():
        term = {(): coefficient}
        for i in mon:
            term = mul(term, values[i], p)
        out = add(out, term, p)
    return out


def evaluate(poly, values, p):
    total = 0
    for mon, coefficient in poly.items():
        for i in mon:
            coefficient = coefficient * values[i] % p
        total += coefficient
    return total % p


def pack(polys):
    return [[[c, list(mon)] for mon, c in sorted(poly.items())] for poly in polys]


def unpack(polys):
    return [{tuple(mon): c for c, mon in poly} for poly in polys]


def rref(matrix, columns, p):
    """Reduce an augmented matrix; pivot only within its first columns columns."""
    rows = [[v % p for v in row] for row in matrix]
    pivots = []
    for col in range(columns):
        pivot = next((i for i in range(len(pivots), len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        k = len(pivots)
        rows[k], rows[pivot] = rows[pivot], rows[k]
        inverse = pow(rows[k][col], -1, p)
        rows[k] = [v * inverse % p for v in rows[k]]
        for i in range(len(rows)):
            if i != k and rows[i][col]:
                factor = rows[i][col]
                rows[i] = [(a - factor * b) % p for a, b in zip(rows[i], rows[k])]
        pivots.append(col)
    return rows, pivots


def rank_of(rows, columns, p):
    return len(rref(rows, columns, p)[1])


def invert(matrix, p):
    n = len(matrix)
    rows, pivots = rref(
        [row + [int(i == j) for j in range(n)] for i, row in enumerate(matrix)], n, p
    )
    if len(pivots) != n:
        raise ValueError("Singular matrix")
    return [row[n:] for row in rows]


def linear_solutions(matrix, rhs, columns, p, limit):
    """Enumerate every solution, including singular but consistent systems."""
    rows, pivots = rref([row + [b] for row, b in zip(matrix, rhs)], columns, p)
    if any(not any(row[:columns]) and row[-1] for row in rows):
        return
    free = [j for j in range(columns) if j not in pivots]
    if p ** len(free) > limit:
        raise ValueError("Too many preimages; increase the explicit search limit")
    for values in itertools.product(range(p), repeat=len(free)):
        solution = [0] * columns
        for j, value in zip(free, values):
            solution[j] = value
        for i, j in enumerate(pivots):
            solution[j] = (rows[i][-1] - sum(rows[i][k] * solution[k] for k in free)) % p
        yield solution


def affine(matrix, offset, vector, p):
    return [(sum(a * b for a, b in zip(row, vector)) + c) % p
            for row, c in zip(matrix, offset)]


def random_affine(n, p, rng):
    while True:
        matrix = [[rng.randrange(p) for _ in range(n)] for _ in range(n)]
        try:
            inverse = invert(matrix, p)
            return matrix, [rng.randrange(p) for _ in range(n)], inverse
        except ValueError:
            pass


def random_quadratic(n, p, rng, vinegar=None):
    monomials = [()] + [(i,) for i in range(n)]
    monomials += [(i, j) for i in range(n) for j in range(i, n)
                  if vinegar is None or i < vinegar or j < vinegar]
    return {mon: c for mon in monomials if (c := rng.randrange(p))}


def validate_parameters(p, n, m, t, s):
    if p < 3 or not p % 2 or any(p % d == 0 for d in range(3, math.isqrt(p) + 1, 2)):
        raise ValueError("p must be an odd prime")
    if not 1 <= t <= min(n, m):
        raise ValueError("Require 1 <= t <= min(n, m)")
    if not 1 <= s <= n - t - 1:
        raise ValueError("Require at least one oil variable: 1 <= s <= n-t-1")
    if m < t + 1:
        raise ValueError("Require m > t so the U layer is non-empty")
    if m - (n - s) < 3:
        raise ValueError("Require m >= n - s + 3 for essentially unique preimages")


def keygen(p=17, n=9, m=11, t=3, s=2, rng=None):
    """Build actual expanded public polynomials, never expose the decomposition."""
    validate_parameters(p, n, m, t, s)
    rng = rng if rng is not None else secrets.SystemRandom()
    a1, b1, a1_inverse = random_affine(m, p, rng)
    a2, b2, a2_inverse = random_affine(n, p, rng)
    qmap = [random_quadratic(n - t, p, rng) for _ in range(t)]
    umap = [random_quadratic(n, p, rng, t + s) for _ in range(m - t)]
    z = [{(): b, **{(i,): c for i, c in enumerate(row) if c}}
         for row, b in zip(a2, b2)]
    w = [add(z[i], substitute(qmap[i], z[t:], p), p, -1) for i in range(t)]
    central = w + [substitute(poly, w + z[t:], p) for poly in umap]
    public_polys = []
    for row, b in zip(a1, b1):
        poly = {(): b} if b else {}
        for coefficient, component in zip(row, central):
            poly = add(poly, component, p, coefficient)
        public_polys.append(poly)
    parameters = dict(p=p, n=n, m=m, t=t, s=s)
    public = dict(kind="public", parameters=parameters, polynomials=pack(public_polys))
    private = dict(kind="private", parameters=parameters,
                   A1=a1, b1=b1, A1_inverse=a1_inverse,
                   A2=a2, b2=b2, A2_inverse=a2_inverse, q=pack(qmap), U=pack(umap))
    return public, private


def check_vector(vector, size, p):
    if len(vector) != size or any(type(x) is not int or not 0 <= x < p for x in vector):
        raise ValueError(f"Expected {size} field elements in [0, {p})")


def encrypt_vector(public, vector):
    params = public['parameters']
    check_vector(vector, params['n'], params['p'])
    return [evaluate(poly, vector, params['p']) for poly in unpack(public['polynomials'])]


def secret_evaluate(private, vector):
    p, t = private['parameters']['p'], private['parameters']['t']
    z = affine(private['A2'], private['b2'], vector, p)
    w = [(z[i] - evaluate(poly, z[t:], p)) % p for i, poly in enumerate(unpack(private['q']))]
    central = w + [evaluate(poly, w + z[t:], p) for poly in unpack(private['U'])]
    return affine(private['A1'], private['b1'], central, p)


def decrypt_vector(private, ciphertext, limit=100000):
    par = private['parameters']
    p, n, m, t, s = (par[k] for k in ('p', 'n', 'm', 't', 's'))
    check_vector(ciphertext, m, p)
    if p ** s > limit:
        raise ValueError("Vinegar enumeration exceeds the explicit search limit")
    c = affine(private['A1_inverse'], [0] * m,
               [(v - b) % p for v, b in zip(ciphertext, private['b1'])], p)
    qmap, umap = unpack(private['q']), unpack(private['U'])
    oils = n - t - s
    answers = []
    for vinegar in itertools.product(range(p), repeat=s):
        base = c[:t] + list(vinegar) + [0] * oils
        constants = [evaluate(poly, base, p) for poly in umap]
        matrix = [[] for _ in umap]
        for j in range(oils):
            probe = base.copy()
            probe[t + s + j] = 1
            for i, poly in enumerate(umap):
                matrix[i].append((evaluate(poly, probe, p) - constants[i]) % p)
        rhs = [(v - b) % p for v, b in zip(c[t:], constants)]
        for oil in linear_solutions(matrix, rhs, oils, p, max(limit - len(answers), 0)):
            y = list(vinegar) + oil
            x = [(v + evaluate(poly, y, p)) % p for v, poly in zip(c[:t], qmap)]
            shifted = [(v - b) % p for v, b in zip(x + y, private['b2'])]
            answers.append(affine(private['A2_inverse'], [0] * n, shifted, p))
    return answers


def byte_width(p):
    width = 1
    while p ** width < 256:
        width += 1
    return width


def encode_frame(plaintext, p, n):
    """Length || data as fixed-width, big-endian base-p digits, then zero padding."""
    width = byte_width(p)
    frame = len(plaintext).to_bytes(4, 'big') + plaintext
    digits = []
    for value in frame:
        digits.extend((value // (p ** i)) % p for i in reversed(range(width)))
    return digits + [0] * (-len(digits) % n)


def decode_frame(digits, p, n):
    width = byte_width(p)
    if len(digits) < 4 * width:
        raise ValueError("Missing length header")

    def decode_byte(start):
        value = 0
        for digit in digits[start:start + width]:
            value = value * p + digit
        if value > 255:
            raise ValueError("Preimage is not a byte block")
        return value

    length = int.from_bytes(bytes(decode_byte(i * width) for i in range(4)), 'big')
    end = (4 + length) * width
    if end > len(digits) or len(digits) != ((end + n - 1) // n) * n or any(digits[end:]):
        raise ValueError("Invalid length or padding")
    return bytes(decode_byte(i) for i in range(4 * width, end, width))


def try_decode_frame(digits, p, n):
    try:
        return decode_frame(digits, p, n)
    except ValueError:
        return None


def encrypt_bytes(public, plaintext):
    par = public['parameters']
    n = par['n']
    frame = encode_frame(plaintext, par['p'], n)
    return dict(kind="ciphertext", parameters=par,
                blocks=[encrypt_vector(public, list(frame[i:i+n])) for i in range(0, len(frame), n)])


def main(argv):
    rng = secrets.SystemRandom()
    public, private = keygen(**PARAMETERS, rng=rng)
    ciphertext = encrypt_bytes(public, FLAG.encode('utf-8'))
    output = {"public_key": public, "ciphertext": ciphertext}
    assert "private" not in output and "A1" not in json.dumps(output)
    with open("out.txt", "w") as fh:
        json.dump(output, fh, separators=(",", ":"))


if __name__ == '__main__':
    main(sys.argv[1:])

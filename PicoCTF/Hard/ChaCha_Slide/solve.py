#!/usr/bin/env python3
# %%
from CTF_Crypto_Attack.Util import BaseSocketOracle, parsers
from sage.all import *
from pwn import remote

io = remote("xebec.cylabacademy.net", 32195)
mask = 0x0ffffffc0ffffffc0ffffffc0fffffff
goal = b"But it's only secure if used correctly!"

class Oracle(BaseSocketOracle):
    def get_all(self):
        return parsers(self.io.recv().strip().decode(), parse_hex=True, multi_value=True, normalize_keys=True).values()

def poly_coeffs(ct=b'', ad=b''):
    pad_ad = ad + b'\x00' * ((16 - len(ad) % 16) % 16)
    pad_ct = ct + b'\x00' * ((16 - len(ct) % 16) % 16)
    lengths = len(ad).to_bytes(8, 'little') + len(ct).to_bytes(8, 'little')
    data = pad_ad + pad_ct + lengths

    coeffs = []
    for i in range(0, len(data), 16):
        block = data[i:i+ 16]
        c_i = int.from_bytes(block, 'little') + (1 << 128)
        coeffs.append(c_i)
    return coeffs

def main() -> None:
    oracle = Oracle(io)
    plaintext, plaintext_hex, ciphertext_hex = oracle.get_all()

    C1, T1, N1 = ciphertext_hex[0][:-28], ciphertext_hex[0][-28:-12], ciphertext_hex[0][-12:]
    C2, T2, N2 = ciphertext_hex[1][:-28], ciphertext_hex[1][-28:-12], ciphertext_hex[1][-12:]

    t1, t2 = int.from_bytes(T1, 'little'), int.from_bytes(T2, 'little')
    c1_l = poly_coeffs(C1)
    c2_l = poly_coeffs(C2)
    assert N1 == N2

    poly = PolynomialRing(GF(2**130 - 5), 'r')
    r = poly.gen()

    def build_poly(coeffs):
        f = 0
        for c in coeffs:
            f = (f + c) * r
        return f

    g1 = build_poly(c1_l)
    g2 = build_poly(c2_l)

    r_found, s_found = False, False
    for k in range(-4, 5):
        diff = (t1 - t2) + k * (1 << 128)
        eq = g1 - g2 - diff

        for root, _ in eq.roots():
            cand_r = int(root)
            if (cand_r & mask) == cand_r:
                r_found = cand_r
                s_found = (t1 - int(g1(cand_r))) % (1 << 128)
                break
        if r_found:
            break

    keystream = bytes(a ^ b for a, b in zip(C1, plaintext_hex[0]))
    C_goal = bytes(a ^ b for a, b in zip(goal, keystream))
    g = build_poly(poly_coeffs(C_goal))
    T_goal = ((int(g(r_found)) + s_found) % (1 << 128)).to_bytes(16, 'little')

    payload = C_goal + T_goal + N1
    io.sendline(payload.hex().encode())
    print(io.recvall().strip().decode())
if __name__ == "__main__":
    main()

# %%

from CTF_Crypto_Attack.Util import BaseHttpOracle, magical_decode
from sage.all import *

base_url = "https://aes.cryptohack.org/forbidden_fruit"

def main():
    oracle = BaseHttpOracle(base_url)
    def encrypt(plaintext):
        data = oracle.get_json(f"encrypt/{plaintext.hex()}/")
        return list(map(bytes.fromhex, [data['nonce'], data['ciphertext'], data['tag'], data['associated_data']]))
    def decrypt(nonce, ciphertext, tag, associated_data):
        return oracle.get_json(f"decrypt/{nonce.hex()}/{ciphertext.hex()}/{tag.hex()}/{associated_data.hex()}/")
    def cal_stream(A, C):
        A_pad = A + b"\x00" * ((-len(A)) % 16)
        C_pad = C + b"\x00" * ((-len(C)) % 16)
        L = (len(A) * 8).to_bytes(8, 'big') + (len(C) * 8).to_bytes(8, 'big')
        return A_pad + C_pad + L
    def _bytes_to_ghash_elem(block: bytes):
        val = int.from_bytes(block, "big")
        bits = [(val >> (127 - i)) & 1 for i in range(128)]
        return GF128(bits)
    def _ghash_elem_to_bytes(elem) -> bytes:
        poly = elem.polynomial()
        val = 0
        for i in range(128):
            if poly[i]:
                val |= 1 << (127 - i)
        return val.to_bytes(16, 'big')
    def stream_to_elems(stream):
        return [_bytes_to_ghash_elem(stream[i:i + 16]) for i in range(0, len(stream), 16)]
    def ghash(blocks, h_val):
        g = 0
        for b in blocks:
            g = (g + b) * h_val
        return g
    N0, C0, T0, A0 = encrypt(b"\x00" * 16)
    N1, C1, T1, A1 = encrypt(b"\x01" * 16)

    P_2 = PolynomialRing(GF(2), "x")
    x = P_2.gen()
    GF128 = GF(2**128, name='a', modulus=x**128 + x**7 + x**2 + x + 1)
    P_H = PolynomialRing(GF128, 'H')
    H_var = P_H.gen()

    S0 = cal_stream(A0, C0)
    S1 = cal_stream(A1, C1)
    blocks0 = stream_to_elems(S0)
    blocks1 = stream_to_elems(S1)
    t0 = _bytes_to_ghash_elem(T0)
    t1 = _bytes_to_ghash_elem(T1)

    poly = ghash(blocks0, H_var) + ghash(blocks1, H_var) + t0 + t1
    h_cand = [r for r, _ in poly.roots()]
    
    P_target = b"give me the flag"
    C_forged = bytes(c ^ p for c, p in zip(C0, P_target))
    blocks_forged = stream_to_elems(cal_stream(A0, C_forged))

    for H in h_cand:
        mask = t0 + ghash(blocks0, H)
        t_forged_elem = ghash(blocks_forged, H) + mask
        T_forged = _ghash_elem_to_bytes(t_forged_elem)
        res = decrypt(N0, C_forged, T_forged, A0)
        try:
            flag = magical_decode(res['plaintext'])
            print(flag)
        except Exception:
            print(res)
if __name__ == '__main__':
    main()

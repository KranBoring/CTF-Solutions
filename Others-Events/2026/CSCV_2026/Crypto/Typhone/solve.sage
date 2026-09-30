import json
import hashlib
import struct
import re
import sys
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long as B2L, long_to_bytes as L2B
from sage.all import *

def log(msg):
    print(msg, flush=True)

def aes_gcm_decrypt(key, nonce_hex, ct_hex, tag_hex):
    return AES.new(key, AES.MODE_GCM, nonce=bytes.fromhex(nonce_hex)).decrypt_and_verify(
        bytes.fromhex(ct_hex), bytes.fromhex(tag_hex)
    )

def main():
    log("[*] Đang đọc file output_typhon.txt...")
    with open("output_typhon.txt", "r") as f:
        data = json.load(f)

    # =============================================================
    # TẦNG 1 & 2: LCG & Håstad Broadcast Attack
    # =============================================================
    try:
        log("[*] Stage 1 & 2: Bẻ khóa LCG và Håstad...")
        LM = int(data["α"]["M"])
        lo = [int(x) for x in data["α"]["out"]]
        dx0 = (lo[1] - lo[0]) % LM
        dx1 = (lo[2] - lo[1]) % LM
        La = int((dx1 * inverse_mod(dx0, LM)) % LM)
        Lc = int((lo[1] - La * lo[0]) % LM)
        x5 = int((La * lo[4] + Lc) % LM)

        k0 = hashlib.sha256(L2B(x5, 16)).digest()[:16]
        bp = aes_gcm_decrypt(k0, data["α"]["Φ"]["N"], data["α"]["Φ"]["C"], data["α"]["Φ"]["T"])
        
        Hn = [B2L(bp[i*16:(i+1)*16]) for i in range(3)]
        Hc = [B2L(bp[(i+3)*16:(i+4)*16]) for i in range(3)]
        
        Mh = int(Integer(crt(Hc, Hn)).nth_root(3))
        Kw = hashlib.sha256(L2B(Mh, 15)).digest()[:16]
    except Exception as e:
        log(f"[!] Lỗi Stage 1-2: {e}")
        return

    # =============================================================
    # TẦNG 3: Khôi phục lf qua AES-GCM Nonce Reuse
    # =============================================================
    try:
        log("[*] Stage 3: Khôi phục lf qua AES-GCM Nonce Reuse...")
        gamma_raw = aes_gcm_decrypt(Kw, data["γ"]["Φ"]["N"], data["γ"]["Φ"]["C"], data["γ"]["Φ"]["T"])
        gamma_json = json.loads(gamma_raw)

        P1 = bytes.fromhex(gamma_json["p1"])
        C1 = bytes.fromhex(gamma_json["c1"])
        C2 = bytes.fromhex(gamma_json["c2"])

        # Nonce reuse: P2 = C1 ^ C2 ^ P1, 8 byte đầu tiên là lf
        lf = bytes([c1 ^ c2 ^ p1 for c1, c2, p1 in zip(C1, C2, P1)])[:8]
        log(f"[+] Stage 3 thành công! lf = {lf.hex()}")
    except Exception as e:
        log(f"[!] Lỗi Stage 3: {e}")
        return

    # =============================================================
    # TẦNG 4 & 5: LFSR 32-bit & Pohlig-Hellman DLP
    # =============================================================
    try:
        log("[*] Stage 4 & 5: LFSR 32-bit & Pohlig-Hellman DLP...")
        lf_bits = [(int.from_bytes(lf, 'big') >> (63 - i)) & 1 for i in range(64)]
        st = sum(lf_bits[i] << i for i in range(32))
        
        for _ in range(64):
            fb = 0
            for t in [32, 30, 26, 24]: fb ^= (st >> (t - 1)) & 1
            st = (st >> 1) | (fb << 31)

        kL_val = 0
        for _ in range(128):
            b, fb = st & 1, 0
            for t in [32, 30, 26, 24]: fb ^= (st >> (t - 1)) & 1
            st = (st >> 1) | (fb << 31)
            kL_val = (kL_val << 1) | b
            
        delta = json.loads(aes_gcm_decrypt(kL_val.to_bytes(16, 'big'), data["δ"]["Φ"]["N"], data["δ"]["Φ"]["C"], data["δ"]["Φ"]["T"]))
        F = GF(int(delta["ph_p"]))
        Px = int(discrete_log(F(int(delta["ph_h"])), F(int(delta["ph_g"]))))
        KE = hashlib.sha256(L2B(Px, 16)).digest()[:16]
    except Exception as e:
        log(f"[!] Lỗi Stage 4-5: {e}")
        return

    # =============================================================
    # TẦNG 6: SHA-256 Length Extension
    # =============================================================
    try:
        log("[*] Stage 6: SHA-256 Length Extension...")
        zeta = json.loads(aes_gcm_decrypt(KE, data["ζ"]["Φ"]["N"], data["ζ"]["Φ"]["C"], data["ζ"]["Φ"]["T"]))
        Sm, SM, sl = zeta["sha_mac"], bytes.fromhex(zeta["sha_msg"]), int(zeta["secret_len"])

        SK = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
              0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
              0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
              0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
              0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
              0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
              0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
              0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

        rr = lambda x, n: ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF
        def sp(n): return b'\x80' + b'\x00' * ((55 - n) % 64) + struct.pack('>Q', n * 8)
        
        st = [int.from_bytes(bytes.fromhex(Sm)[i:i+4], 'big') for i in range(0, 32, 4)]
        bl = b"::uid=root::op=exec" + sp(sl + len(SM) + len(b"::uid=root::op=exec") + len(sp(sl + len(SM))))
        
        for i in range(0, len(bl), 64):
            w = list(struct.unpack('>16I', bl[i:i+64]))
            for j in range(16, 64):
                w.append((w[j-16] + (rr(w[j-15],7)^rr(w[j-15],18)^(w[j-15]>>3)) + w[j-7] + (rr(w[j-2],17)^rr(w[j-2],19)^(w[j-2]>>10))) & 0xFFFFFFFF)
            a,b,c,d,e,f,g,h = st
            for j in range(64):
                t1 = (h + (rr(e,6)^rr(e,11)^rr(e,25)) + ((e&f)^(~e&g)) + SK[j] + w[j]) & 0xFFFFFFFF
                t2 = ((rr(a,2)^rr(a,13)^rr(a,22)) + ((a&b)^(a&c)^(b&c))) & 0xFFFFFFFF
                h,g,f,e,d,c,b,a = g,f,e, (d+t1)&0xFFFFFFFF, c,b,a, (t1+t2)&0xFFFFFFFF
            st = [(st[idx] + v) & 0xFFFFFFFF for idx, v in enumerate([a,b,c,d,e,f,g,h])]
            
        kS = b''.join(struct.pack('>I', s) for s in st)[:16]
        Ke = hashlib.sha256(kS).digest()[:16]
    except Exception as e:
        log(f"[!] Lỗi Stage 6: {e}")
        return

    # =============================================================
    # TẦNG 7 & 8: Tách C2 Beacon & RAT Config
    # =============================================================
    try:
        log("[*] Stage 7 & 8: Dịch ngược Cấu hình C2 và RAT...")
        cc_plain = aes_gcm_decrypt(Ke, data["η"]["Φ"]["N"], data["η"]["Φ"]["C"], data["η"]["Φ"]["T"]).decode()
        hosts = ["ws-alpha", "ws-bravo", "ws-charlie", "ws-delta", "ws-echo", "ws-foxtrot", "ws-golf", "ws-hotel",
                 "ws-india", "ws-juliet", "ws-kilo", "ws-lima", "ws-mike", "ws-november", "ws-oscar", "ws-papa"]
        key_cc_list = [0] * 16
        for b_val, h_name in re.findall(r'BEACON #(\d+)\s+(ws-\w+)', cc_plain):
            if h_name in hosts: key_cc_list[hosts.index(h_name)] = int(b_val)
        
        Kcc = hashlib.sha256(bytes(key_cc_list)).digest()[:16]
        ratdata = json.loads(aes_gcm_decrypt(Kcc, data["θ"]["Φ"]["N"], data["θ"]["Φ"]["C"], data["θ"]["Φ"]["T"]).decode())
        
        mnames = ["keylogger", "screencap", "filegrab", "shellexec", "clipboard", "browser_stealer",
                  "credential_dump", "network_scan", "lateral_move", "persistence", "exfil", "c2_rotate",
                  "av_evasion", "process_inject", "memory_scan", "log_wipe"]
        key_rat = bytes(next(m["interval"] for m in ratdata["modules"] if m["name"] == mn) for mn in mnames)
        Krat = hashlib.sha256(key_rat).digest()[:16]
    except Exception as e:
        log(f"[!] Lỗi Stage 7-8: {e}")
        return

    # =============================================================
    # TẦNG 9: ECDSA HNP via LLL
    # =============================================================
    try:
        log("[*] Stage 9: Giải mã Nonce ECDSA qua LLL...")
        iota = json.loads(aes_gcm_decrypt(Krat, data["ι"]["Φ"]["N"], data["ι"]["Φ"]["C"], data["ι"]["Φ"]["T"]))
        tb = aes_gcm_decrypt(kS, iota["tx_nonce"], iota["tx_ct"], iota["tx_tag"])
        EN = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

        TX = [(int.from_bytes(tb[i*96:i*96+32], 'big'), int.from_bytes(tb[i*96+32:i*96+64], 'big'), int.from_bytes(tb[i*96+64:(i+1)*96], 'big')) for i in range(6)]
        ti = [(int(inverse_mod(s, EN)) * r) % EN for r, s, z in TX]
        ui = [(int(inverse_mod(s, EN)) * z) % EN for r, s, z in TX]

        t0_inv = int(inverse_mod(ti[0], EN))
        c_coeffs = [(ti[i] * t0_inv) % EN for i in range(1, 6)]
        d_coeffs = [(ui[i] - c_coeffs[i-1] * ui[0]) % EN for i in range(1, 6)]

        M_lat = matrix(ZZ, 7, 7)
        for i in range(5): M_lat[i, i] = EN
        for i in range(5): M_lat[5, i] = c_coeffs[i]
        M_lat[5, 5] = 1
        for i in range(5): M_lat[6, i] = d_coeffs[i]
        M_lat[6, 6] = 2**128

        E = EllipticCurve(GF(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F), [0, 7])
        G = E(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
        Q_pub = E(int(data["pub"]["Qx"]), int(data["pub"]["Qy"]))

        de = next((int(cand_de) for row in M_lat.LLL() for k0_val in [abs(int(row[5])), EN - abs(int(row[5]))] 
                   if k0_val != 0 and (cand_de := ((k0_val - ui[0]) * t0_inv) % EN) > 0 and cand_de * G == Q_pub), None)
        
        if de is None: raise ValueError("LLL không tìm ra khóa ECDSA")
        K_ec = hashlib.sha256(L2B(de, 32)).digest()[:16]
    except Exception as e:
        log(f"[!] Lỗi Stage 9: {e}")
        return

    # =============================================================
    # TẦNG 10 & 11: Boneh-Durfee & Coppersmith
    # =============================================================
    try:
        log("[*] Stage 10 & 11: Chạy Boneh-Durfee và Coppersmith Attack...")
        kd = json.loads(aes_gcm_decrypt(K_ec, data["κ"]["Φ"]["N"], data["κ"]["Φ"]["C"], data["κ"]["Φ"]["T"]))
        n_bd, e_bd, c_bd = Integer(kd["n"]), Integer(kd["e"]), Integer(kd["c"])

        m, t, X, Y, A = 4, 1, floor(2 * RealField(1000)(n_bd)**0.28), floor(3 * RealField(1000)(n_bd)**0.5), n_bd + 1
        P = PolynomialRing(ZZ, names=('x', 'y'))
        x, y = P.gens()
        f = 1 + x * (A - y)
        
        polys = [x**i * f**k * e_bd**(m - k) for k in range(m + 1) for i in range(m - k + 1)] + \
                [y**j * f**k * e_bd**(m - k) for j in range(1, t + 1) for k in range(j, m + 1)]
        monos = sorted(list(set(mono for p in polys for mono in p.monomials())))
        
        M = matrix(ZZ, len(polys), len(polys))
        for i, p in enumerate(polys):
            for j, mono in enumerate(monos):
                M[i, j] = p.monomial_coefficient(mono) * mono(X, Y)
                
        M_red = M.LLL()
        h1 = sum(ZZ(M_red[0, j] // monos[j](X, Y)) * monos[j] for j in range(len(polys)))
        h2 = sum(ZZ(M_red[1, j] // monos[j](X, Y)) * monos[j] for j in range(len(polys)))
        
        res = h1.resultant(h2, y)
        d_bd = next((int(inverse_mod(e_bd, n_bd + 1 - int(s_val))) for r, _ in res.univariate_polynomial().roots()
                     if (k_val := abs(int(r))) != 0 for s_val, _ in h1(x=k_val).univariate_polynomial().roots()
                     if (phi := n_bd + 1 - int(s_val)) > 0 and (e_bd * inverse_mod(e_bd, phi) - 1) % phi == 0), None)
        
        if d_bd is None: raise ValueError("Boneh-Durfee không tìm ra d_bd")

        key_bd = hashlib.sha256(L2B(int(pow(c_bd, d_bd, n_bd)), 16)).digest()[:16]

        ld = json.loads(aes_gcm_decrypt(key_bd, data["λ"]["Φ"]["N"], data["λ"]["Φ"]["C"], data["λ"]["Φ"]["T"]))
        n_cop, p_known = int(ld["n"]), int(ld["p_top"]) << 128
        roots = (PolynomialRing(Zmod(n_cop), names=('x',)).gen() + p_known).monic().small_roots(X=2**128, beta=0.5, epsilon=0.03)
        p_cop = next((int(p_known + r) for r in roots if n_cop % int(p_known + r) == 0), None)
        
        if p_cop is None: raise ValueError("Coppersmith không hội tụ")
    except Exception as e:
        log(f"[!] Lỗi Stage 10-11: {e}")
        return

    # =============================================================
    # TẦNG 12: FLAG FINAL
    # =============================================================
    try:
        MASTER = hashlib.sha256(
            kL_val.to_bytes(16, 'big') + L2B(Px, 16) + 
            kS + bytes(key_cc_list) + key_rat + key_bd + hashlib.sha256(L2B(int(p_cop), 32)).digest()[:16]
        ).digest()
        
        flag = aes_gcm_decrypt(MASTER, data['Ω']['N'], data['Ω']['C'], data['Ω']['T']).decode()
        log("\n" + "=" * 50 + f"\n[SUCCESS] FLAG TÌM THẤY: {flag}\n" + "=" * 50)
    except Exception as e:
        log(f"[!] Lỗi giải mã Master Key: {e}")

if __name__ == "__main__":
    sys.set_int_max_str_digits(0)
    main()
#!/usr/bin/env python3
from CTF_Crypto_Attack.Symmetric import forge_gcm_tag, recover_gcm_hash_key
from CTF_Crypto_Attack.Util import BaseHttpOracle, magical_decode

base_url = "https://aes.cryptohack.org/forbidden_fruit"

def main() -> None:
    oracle = BaseHttpOracle(base_url)
    def encrypt(plaintext):
        data = oracle.get_json(f"encrypt/{plaintext.hex()}/")
        return list(map(bytes.fromhex, [data['nonce'], data['ciphertext'], data['tag'], data['associated_data']]))
    
    def decrypt(nonce, ciphertext, tag, associated_data):
        return oracle.get_json(f"decrypt/{nonce.hex()}/{ciphertext.hex()}/{tag.hex()}/{associated_data.hex()}/")

    P0 = b"A" * 16
    P1 = b"B" * 16
    N0, C0, T0, A0 = encrypt(P0)
    N1, C1, T1, A1 = encrypt(P1)

    h_cand = recover_gcm_hash_key(A0, C0, T0, A1, C1, T1)

    P_target = b"give me the flag"
    C_forged = bytes(c ^ p ^ fake_p for c, p, fake_p in zip(C0, P0, P_target))

    for H in h_cand:
        T_forged = forge_gcm_tag(H, A0, C0, T0, A0, C_forged)
        res = decrypt(N0, C_forged, T_forged, A0)
        try:
            flag = magical_decode(res['plaintext'])
            print(flag)
        except Exception:
            print(res)
if __name__ == "__main__":
    main()

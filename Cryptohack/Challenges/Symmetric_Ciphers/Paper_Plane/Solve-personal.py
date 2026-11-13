from CTF_Crypto_Attack.Symmetric import get_intermediate_block
from CTF_Crypto_Attack.Util import BaseHttpOracle
from Crypto.Util.Padding import unpad
from pwn import xor
from concurrent.futures import ThreadPoolExecutor
from time import time

class Oracle(BaseHttpOracle):
    def __init__(self, base_url, prev_m=b"", pool_size = 256):
        super().__init__(base_url, pool_size=pool_size)
        self.prev_m = prev_m

    def is_padding_valid(self, ct):
        fake_c0 = ct[:16].hex()
        cipher = ct[16:].hex()
        m0_hex = self.prev_m.hex()

        endpoint = f"send_msg/{cipher}/{m0_hex}/{fake_c0}/"
        data = self.get_json(endpoint)
        return 'msg' in data

    def check_batch(self, cts):
        with ThreadPoolExecutor(max_workers=len(cts)) as f:
            return list(f.map(self.is_padding_valid, cts))

def main():
    base_url = "https://aes.cryptohack.org/paper_plane/"
    oracle = Oracle(base_url)
    
    init_data = oracle.get_json("encrypt_flag/")
    ciphertext = bytes.fromhex(init_data['ciphertext'])
    c0 = bytes.fromhex(init_data['c0'])
    m0 = bytes.fromhex(init_data['m0'])
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    prev_c = c0
    oracle.prev_m = m0
    full_plaintext = bytearray()
    flag_alphabet = b"crypto{h3l0_lg4m}\x0a"

    for idx, curr_c in enumerate(blocks):
        print(f"\n[*] Đang giải mã Khối {idx + 1}/{len(blocks)}...")
        I = get_intermediate_block(
            target_block=curr_c,
            oracle=oracle,
            prev_block_for_charset=prev_c,
            charset=flag_alphabet,
            batch_size=len(flag_alphabet),
            debug=True,
            block_idx=idx
        )
        P_i = xor(I, prev_c)
        full_plaintext.extend(P_i)
        oracle.prev_m = P_i
        prev_c = curr_c

    flag = unpad(bytes(full_plaintext), 16).decode()
    print(flag)

if __name__ == '__main__':
    start = time()
    main()
    print(f"Thời gian chạy: {time() - start}")

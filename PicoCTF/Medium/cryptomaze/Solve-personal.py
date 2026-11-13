#!/usr/bin/env python3
from CTF_Crypto_Attack.Symmetric import lfsr_keystream_generator
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
def main() -> None:
    lsfr = [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1]
    taps = [63, 61, 60, 58]
    ciphertext = bytes.fromhex("5fdec2e502a7c8d5951f41da4b0e0057fa1c4a5dcf3ecb8affd53e58f05cdfb138338e7e04fbddef0c6260a4eb758417")
    keystream = lfsr_keystream_generator(lsfr, taps, 16 * 8)
    key = b''.join([long_to_bytes(int(''.join([str(k) for k in keystream[i: i + 8]]), 2)) for i in range(0, len(keystream), 8)])
    cipher = AES.new(key, AES.MODE_ECB)
    flag = cipher.decrypt(ciphertext)
    print(flag.decode())
if __name__ == "__main__":
    main()
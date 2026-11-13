#!/usr/bin/env python3
from codecs import decode

def main() -> None:
    
    ciphertext = "npnqrzl{abg_gbb_onq_bs_n_ceboyrz}"
    print(decode(ciphertext, 'rot_13'))

if __name__ == "__main__":
    main()
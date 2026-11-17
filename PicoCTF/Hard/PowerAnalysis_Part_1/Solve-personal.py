#!/usr/bin/env python3
import numpy as np 
from CTF_Crypto_Attack.SCA import SCA_first_order_AES

def main() -> None:
    plaintexts = np.load("plaintexts.npy")
    traces = np.load("traces.npy")
    key = SCA_first_order_AES(plaintexts, traces, window=(300,400), debug=True, format='hex')
    print(f"academy{{{key}}}")

if __name__ == "__main__":
    main()

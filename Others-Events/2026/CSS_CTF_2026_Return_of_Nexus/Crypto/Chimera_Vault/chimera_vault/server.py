#!/usr/bin/env python3
import os
import sys
import math
import struct
import base64
import random
import signal
from Crypto.Util.number import getPrime, inverse, bytes_to_long

FLAG = os.environ.get("FLAG", "CSSCTF{I_4m_r0ck_f4k3}")
MOD_BITS = 128

def generate_carrier_burst(token: int) -> str:
    sample_rate = 8000
    duration = 0.8
    num_samples = int(sample_rate * duration)
    
    # Frequencies derived from token
    f1 = 440 + (token & 0xFF) * 5
    f2 = 1200 + ((token >> 8) & 0xFF) * 5
    
    raw_pcm = bytearray()
    for i in range(num_samples):
        t = i / sample_rate
        val = 0.4 * math.sin(2 * math.pi * f1 * t) + 0.4 * math.sin(2 * math.pi * f2 * t)
        val += random.gauss(0, 0.05)
        sample = int(max(-1.0, min(1.0, val)) * 32767)
        raw_pcm.extend(struct.pack("<h", sample))
        
    return base64.b64encode(raw_pcm).decode()

class ChimeraVault:
    def __init__(self):
        self.p = getPrime(MOD_BITS // 2)
        self.q = getPrime(MOD_BITS // 2)
        self.N = self.p * self.q
        
        self.session_token = random.randint(0x1000, 0xEFFF)
        
        self.W = random.randint(2, self.N - 2)
        self.G = [[random.randint(1, self.N - 1) for _ in range(3)] for _ in range(3)]
        
        d1 = random.randint(1, self.N - 1)
        d2 = random.randint(1, self.N - 1)
        d3 = (self.W - d1 - d2) % self.N
        self.D = [[d1, 0, 0], [0, d2, 0], [0, 0, d3]]
        
        self.M = [[random.randint(1, self.N - 1) for _ in range(3)] for _ in range(3)]

        self.knapsack_len = 48
        self.r = [random.randint(10, 50)]
        for _ in range(1, self.knapsack_len):
            self.r.append(sum(self.r) + random.randint(5, 50))

        self.M_mod = sum(self.r) + random.randint(1000, 50000)
        if self.M_mod % 2 == 0:
            self.M_mod += 1

        while True:
            self.W = random.randint(2, self.N - 2)
            if math.gcd(self.W, self.M_mod) == 1:
                break

        d1 = random.randint(1, self.N - 1)
        d2 = random.randint(1, self.N - 1)
        d3 = (self.W - d1 - d2) % self.N
        self.D = [[d1, 0, 0], [0, d2, 0], [0, 0, d3]]
        self.M = [
            [random.randint(1, self.N - 1) for _ in range(3)] for _ in range(3)
        ]

        self.s = [(self.W * ri) % self.M_mod for ri in self.r]
        self.target_bits = [
            random.choice([0, 1]) for _ in range(self.knapsack_len)
        ]
        self.target_sum = sum(
            b * weight for b, weight in zip(self.target_bits, self.s)
        )

    def evolve_matrix(self):
        """M_{k+1} = M_k + D (Trace strictly increments by W mod N)"""
        for i in range(3):
            for j in range(3):
                self.M[i][j] = (self.M[i][j] + self.D[i][j]) % self.N
        return self.M

def matrix_to_str(mat):
    return "[" + ", ".join(f"[{', '.join(str(x) for x in row)}]" for row in mat) + "]"

def main():
    signal.alarm(45)
    vault = ChimeraVault()
    
    print("=" * 65)
    print("      PROJECT CHIMERA: THE RESONANT VAULT    ")
    print("=" * 65)
    print(f"[!] System Modulus N = {vault.N}")
    print(f"[!] Knapsack Modulus M_mod = {vault.M_mod}")
    print("\n--- PHASE 1: ACOUSTIC CARRIER SYNCHRONIZATION ---")
    print("Interception probe returned 8kHz mono PCM telemetry stream (Base64):")
    print(generate_carrier_burst(vault.session_token))
    
    try:
        token_input = input("\nEnter decoded session token (hex, e.g. 0x1234): ").strip()
        user_token = int(token_input, 16)
    except Exception:
        print("[-] Invalid token format. Transmission aborted.")
        return

    if user_token != vault.session_token:
        print("[-] Desynchronization fault: Phase locked carrier rejected.")
        return
        
    print("[+] Phase locked! Session carrier aligned.\n")
    print("--- PHASE 2: NON-COMMUTATIVE MATRIX DRIFT TELEMETRY ---")
    print(f"M_0 = {matrix_to_str(vault.M)}")
    
    for step in range(1, 4):
        evolved = vault.evolve_matrix()
        print(f"M_{step} = {matrix_to_str(evolved)}")
        
    print("\n--- PHASE 3: RESONANT KNAPSACK INTERCEPT ---")
    print(f"Knapsack Public Weights S = {vault.s}")
    print(f"Target Resonance Sum    = {vault.target_sum}")
    
    sol = input("\nEnter 48-bit solution vector (binary string e.g. 10101...): ").strip()
    if len(sol) != vault.knapsack_len or any(c not in '01' for c in sol):
        print("[-] Invalid bitvector dimensions.")
        return
        
    user_bits = [int(c) for c in sol]
    check_sum = sum(b * weight for b, weight in zip(user_bits, vault.s))
    
    if check_sum == vault.target_sum and user_bits == vault.target_bits:
        print(f"\n[+] RESONANCE EQUILIBRIUM ACHIEVED. OVERWRITING MASTER KEY...")
        print(f"[+] Flag: {FLAG}")
    else:
        print("[-] Resonance divergence: Vault purged.")

if __name__ == "__main__":
    main()
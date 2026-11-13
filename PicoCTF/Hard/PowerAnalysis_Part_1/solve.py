from CTF_Crypto_Attack.SCA import W_AES, pearson_correlation
import numpy as np

plaintexts = np.load("plaintexts.npy")
traces = np.load("traces.npy")

key = []

for byte_idx in range(16):
    p_col = plaintexts[:, byte_idx]
    best_k = 0
    best_corr = -1.0
    best_sample = -1

    for k_guess in range(256):
        H = W_AES(p_col, k_guess)
        corr_val, sample_idx = pearson_correlation(H, traces)
        if corr_val > best_corr:
            best_corr = corr_val
            best_k = k_guess
            best_sample = sample_idx
    key.append(best_k)
    print(f"Byte {byte_idx:02d}: {best_k:02x} | Best Corr: {best_corr:.4f} tại sample {best_sample}")

key_hex = bytes(key).hex()
print(f"academy{{{key_hex}}}")
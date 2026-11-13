from pathlib import Path
from CTF_Crypto_Attack.Util.parsers import parsers
from CTF_Crypto_Attack.SCA import SCA_first_order_AES
import numpy as np

traces_data = [
    parsers(f, normalize_keys=True, parse_hex=True)
    for f in sorted(Path("traces/").glob("trace*.txt"))
]
plaintexts = np.array([list(d["plaintext"]) for d in traces_data], dtype=np.uint8)
power_traces = np.array([d["power_trace"] for d in traces_data], dtype=np.float64)
'''
key = []

for byte_id in range(16):
    p_col = plaintexts[:, byte_id]
    best_corr = -1.0
    best_sample = 1
    best_k = 0
    for k_guess in range(256):
        H = W_AES(p_col, k_guess)
        corr, sample_id = pearson_correlation(H, power_traces)
        if best_corr < corr:
            best_corr = corr
            best_sample = sample_id
            best_k = k_guess
    key.append(best_k)
    print(f"Byte {byte_id:02d}: {best_k:02x} | Best Corr: {best_corr:.4f} tại sample {best_sample}")

key_hex = bytes(key).hex()
print(f"academy{{{key_hex}}}")
'''
key = SCA_first_order_AES(plaintexts, power_traces, window=(300,400), debug=True, format='hex')
print(f"academy{{{key}}}")
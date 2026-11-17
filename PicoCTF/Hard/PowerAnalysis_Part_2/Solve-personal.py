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
key = SCA_first_order_AES(plaintexts, power_traces, window=(300,400), debug=True, format='hex')
print(f"academy{{{key}}}")
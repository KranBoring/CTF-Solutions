#!/usr/bin/env python3
"""
CHIMERA - Secure Element firmware attestation module

The RSA keypair is produced inside the secure element by the on-die
key-generation library and never leaves it. `chimera_secret` stands in for
the die's protected storage and is not part of the firmware image.

Host sends a 128-bit challenge; the element answers with an attestation
value derived from its internal token.
"""
import json, os, random
from sympy import isprime, n_order

from chimera_secret import p, q, a, token, FLAG

# ---- key-generation library constants (burned into the firmware) ----
M     = 31721752939659896617792337171084495768312741523809821454149295955199893657462682088273
G     = 17
E     = 65537
BASE  = 3
PBITS = 384
NSAMP = 200

# ---- invariants guaranteed by the on-die key-generation library ----
assert isprime(p) and isprime(q)
assert p.bit_length() == PBITS and q.bit_length() == PBITS
assert 0 <= a < n_order(G, M)                   # library draws a from this range
assert p % M == pow(G, a, M)                    # residue of p is fixed by a
assert token.bit_length() <= 128                # attestation token width

N = p * q                                        # never leaves the element
assert N.bit_length() == 2 * PBITS
assert pow(pow(2, E, N), pow(E, -1, (p - 1) * (q - 1)), N) == 2


def attest(chal: int) -> int:
    """Host challenge -> attestation value."""
    return pow(BASE, token ^ chal, N)


if __name__ == "__main__":
    rng = random.Random(int.from_bytes(os.urandom(16), "big"))
    samples = [[c, attest(c)] for c in
               (rng.randrange(1 << 128) for _ in range(NSAMP))]
    json.dump({"e": E, "base_c": BASE,
               "flag_ct": pow(int.from_bytes(FLAG, "big"), E, N),
               "attestations": samples},
              open("output_chimera.txt", "w"), indent=1)
    print("wrote output_chimera.txt")

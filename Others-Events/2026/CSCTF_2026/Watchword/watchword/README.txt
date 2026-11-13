WATCHWORD — intercepted SABRELINK dispatch traffic
==================================================

intercepts.json : one nonce, three authenticated dispatches tagged under it
  (ciphertext + 16-byte GCM tag each, AES-128-GCM, empty AAD), and one sealed
  master order.

The authentication tags are the 'watchword'. The master order text is sealed
with AES-128-CTR (IV all-zero) under the link's per-nonce tag mask E_K(J0) --
the same value that lets the unit stamp a valid tag. Recover the master order
text; the flag is that text. Do not attack real systems.

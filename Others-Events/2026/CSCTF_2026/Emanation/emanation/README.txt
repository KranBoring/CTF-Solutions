EMANATION / QARVETH-73 analysis corpus
The QARVETH-73 and relay-disruption case are fictional. These are synthetic power traces from a Hamming-weight-plus-noise model, not measurements from a physical device.
Each row models one AES-128 first-round operation on the matching known plaintext. A modeled random delay and a fresh byte mask per row obscure the key-dependent samples.
plaintexts.npy: 8000 x 16 uint8 known plaintext bytes; traces.npy: 8000 x 56 float32 samples. Rows correspond one-to-one.
sealed_order.hex: one fictional order encrypted under the same AES-128 key with CTR mode and an all-zero 16-byte initial counter block. Recover the order text.

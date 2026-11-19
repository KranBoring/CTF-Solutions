from itertools import product
import string

LOWERCASE_OFFSET = ord("a")
ALPHABETb16 = string.ascii_lowercase[:16]


def shift(c, k):
	t1 = ord(c) - LOWERCASE_OFFSET
	t2 = ord(k) - LOWERCASE_OFFSET
	return ALPHABETb16[(t1 - t2) % len(ALPHABETb16)]

def b16_decode(cipher):
	dec = ""
	for i in range(0, len(cipher), 2):
		i1 = ALPHABETb16.index(cipher[i])
		i2 = ALPHABETb16.index(cipher[i + 1])
		index = (i1 << 4) + i2
		dec += chr(index)
	return dec


ciphertext = "emfakcakmklfajnnlpekfpkndlmildnmnnljenfckbalpglfnknaonebfcnodkpe"

EVEN_CHARS = {"d", "g"}
ODD_CHARS = set("abcdefghij")

for key_len in range(1, 15):
	valid_per_pos = []
	for pos in range(key_len):
		candidates = []
		for k in ALPHABETb16:
			ok = True
			for i in range(pos, len(ciphertext), key_len):
				p = shift(ciphertext[i], k)
				if (i % 2 == 0 and p not in EVEN_CHARS) or (i % 2 == 1 and p not in ODD_CHARS):
					ok = False
					break
			if ok:
				candidates.append(k)
		valid_per_pos.append(candidates)

	if all(valid_per_pos):
		for key_tuple in product(*valid_per_pos):
			key = "".join(key_tuple)
			b16_plain = "".join(shift(c, key[i % key_len]) for i, c in enumerate(ciphertext))
			flag_body = b16_decode(b16_plain)
			print(f"Key ({key_len}): {key} -> academy{{{flag_body}}}")
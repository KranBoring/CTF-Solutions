from pwn import xor
from CTF_Crypto_Attack.Symmetric import decrypt_affine_ecb,recover_affine_cipher_params

def split(full_key):
	k = full_key
	sub_keys = ["", "", "", ""]
	for i in range(len(k)):
		sub_keys[i % 4] += k[0]
		k = k[1:]
	return sub_keys


def glue(parts):
	k = ""
	for i in range(32):
		k += parts[i % 4][0]
		parts[i % 4] = parts[i % 4][1:]
	return k


def rot_word(word):
	return word[2:] + word[0:2]


def sub_word(word):
	return word


def rcon(word):
	return word


def gen_keys(master_key):
	keys = []
	k = master_key
	for _ in range(11):
		keys.append(k)
		sub_keys = split(k)
		sub_keys[-1] = rcon(sub_word(rot_word(sub_keys[-1])))
		sub_keys[0] = xor(bytes.fromhex(sub_keys[0]), bytes.fromhex(sub_keys[-1])).hex()
		sub_keys[1] = xor(bytes.fromhex(sub_keys[1]), bytes.fromhex(sub_keys[0])).hex()
		sub_keys[2] = xor(bytes.fromhex(sub_keys[2]), bytes.fromhex(sub_keys[1])).hex()
		sub_keys[3] = xor(bytes.fromhex(sub_keys[3]), bytes.fromhex(sub_keys[2])).hex()
		k = glue(sub_keys)
	return keys


def to_matrix(key):
	bytes_list = [int(key[i : i + 2], 16) for i in range(0, 32, 2)]
	array = [[0] * 4 for _ in range(4)]
	for i in range(16):
		array[i % 4][i // 4] = hex(bytes_list[i])[2:]
	return array


def from_matrix(matrix):
	return "".join(matrix[row][col].zfill(2) for col in range(4) for row in range(4))


def sub_bytes(state):
	return state


def shift_rows(state):
	state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
	state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
	state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]
	return state


def gmul(a, b):
	b = int(b, 16)
	p = 0
	for _ in range(8):
		if b & 1:
			p ^= a
		a <<= 1
		if a & 0x100:
			a ^= 0x11B
		b >>= 1
	return p


def mix_columns(s):
	ss = [[0] * 4 for _ in range(4)]
	for c in range(4):
		ss[0][c] = hex(gmul(0x02, s[0][c]) ^ gmul(0x03, s[1][c]) ^ int(s[2][c], 16) ^ int(s[3][c], 16))[2:].zfill(2)
		ss[1][c] = hex(int(s[0][c], 16) ^ gmul(0x02, s[1][c]) ^ gmul(0x03, s[2][c]) ^ int(s[3][c], 16))[2:].zfill(2)
		ss[2][c] = hex(int(s[0][c], 16) ^ int(s[1][c], 16) ^ gmul(0x02, s[2][c]) ^ gmul(0x03, s[3][c]))[2:].zfill(2)
		ss[3][c] = hex(gmul(0x03, s[0][c]) ^ int(s[1][c], 16) ^ int(s[2][c], 16) ^ gmul(0x02, s[3][c]))[2:].zfill(2)
	for i in range(4):
		for j in range(4):
			s[i][j] = ss[i][j]
	return s


def AES(plaintext: str, key: str) -> str:
	ciphertext = plaintext
	round_keys = gen_keys(key)
	ciphertext = xor(bytes.fromhex(round_keys[0]), bytes.fromhex(ciphertext)).hex()
	for i in range(1, 10):
		ciphertext = to_matrix(ciphertext)
		sub_bytes(ciphertext)
		shift_rows(ciphertext)
		mix_columns(ciphertext)
		ciphertext = from_matrix(ciphertext)
		ciphertext = xor(bytes.fromhex(round_keys[i]), bytes.fromhex(ciphertext)).hex()
	ciphertext = to_matrix(ciphertext)
	sub_bytes(ciphertext)
	shift_rows(ciphertext)
	ciphertext = from_matrix(ciphertext)
	ciphertext = xor(bytes.fromhex(round_keys[10]), bytes.fromhex(ciphertext)).hex()
	return ciphertext

def main():
	with open("output.txt") as f:
		ct0, flag_ct = [bytes.fromhex(line.strip()) for line in f.read().splitlines()]
	pt0 = bytes.fromhex("72616e646f6d64617461313131313131")

	def encrypt_zero_key(pt: bytes) -> bytes:
		return bytes.fromhex(AES(pt.hex(), "00" * 16))

	M, K_eff = recover_affine_cipher_params(encrypt_zero_key, known_pair=(pt0, ct0))
	flag = decrypt_affine_ecb(flag_ct, M, K_eff, decode_mode=True)
	print("[+] Flag:", flag)


if __name__ == "__main__":
	main()
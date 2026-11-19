from itertools import product
from Crypto.Cipher import DES
from pwn import remote
from CTF_Crypto_Attack.Symmetric import meet_in_the_middle
from CTF_Crypto_Attack.Util import BaseSocketOracle

io = remote("xebec.cylabacademy.net", 25947)


class Oracle(BaseSocketOracle):
	def get_ciphertext(self) -> bytes:
		self.io.recvline()
		return bytes.fromhex(self.io.recvline().strip().decode())

	def encrypt(self, plaintext: bytes) -> bytes:
		self.io.recvuntil(b"? ")
		self.io.sendline(plaintext.hex().encode())
		return bytes.fromhex(self.io.recvline().strip().decode())


def main():
	oracle = Oracle(io)
	ciphertext = oracle.get_ciphertext()

	pt = b"A" * 8
	ct = oracle.encrypt(pt)[:8]

	keys = [("".join(k) + "  ").encode() for k in product("02468", repeat=6)]

	KEY1, KEY2 = meet_in_the_middle(
		pt=pt,
		ct=ct,
		enc_step=lambda k, data: DES.new(k, DES.MODE_ECB).encrypt(data),
		dec_step=lambda k, data: DES.new(k, DES.MODE_ECB).decrypt(data),
		keyspace_1=keys,
		keyspace_2=keys,
	)

	cipher1 = DES.new(KEY1, DES.MODE_ECB)
	cipher2 = DES.new(KEY2, DES.MODE_ECB)
	flag = cipher1.decrypt(cipher2.decrypt(ciphertext)).rstrip().decode()
	print(flag)


if __name__ == "__main__":
	main()
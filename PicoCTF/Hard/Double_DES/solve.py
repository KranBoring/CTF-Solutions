from CTF_Crypto_Attack.Util import BaseSocketOracle
from Crypto.Cipher import DES
from itertools import product
from pwn import remote
from binascii import unhexlify

io = remote("xebec.cylabacademy.net", 33337)

class Oracle(BaseSocketOracle):
	def get_ciphertext(self):
		self.io.recvline()
		return bytes.fromhex(self.io.recvline().strip().decode())

	def encrypt(self, plaintext):
		self.io.recvuntil(b"? ")
		self.io.sendline(plaintext.hex().encode())
		return bytes.fromhex(self.io.recvline().strip().decode())

def main():
    oracle = Oracle(io)
    ciphertext = oracle.get_ciphertext()

    pt = b"A" * 8
    ct = oracle.encrypt(pt)[:8]

    table = {}
    key = [("".join(k) + "  ").encode() for k in product("02468", repeat=6)]

    for key1 in key:
        cipher = DES.new(key1, DES.MODE_ECB)
        table[cipher.encrypt(pt)] = key1
    for key2 in key:
        cipher = DES.new(key2, DES.MODE_ECB)
        result = cipher.decrypt(ct)
        if result in table:
            KEY1 = table[result]
            KEY2 = key2

    cipher1 = DES.new(KEY1, DES.MODE_ECB)
    cipher2 = DES.new(KEY2, DES.MODE_ECB)
    flag = cipher1.decrypt(cipher2.decrypt(ciphertext)).decode()
    print(flag)

if __name__ == '__main__':
    main()
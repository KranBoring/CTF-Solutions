from CTF_Crypto_Attack.Util import BaseSocketOracle
from CTF_Crypto_Attack.Symmetric import crack_cbc_padding_oracle
from pwn import *
from json import loads, dumps

class Oracle(BaseSocketOracle):
	def check_batch(self, cts):
		format = lambda p: dumps({"option": "unpad", "ct": p.hex()}, separators=(",", ":")).encode()
		self.pipeline_send(cts, format_func=format)
		results = []
		for _ in range(len(cts)):
			res = loads(self.io.recvline().strip().decode())['result']
			results.append(res)
		return results
	def is_padding_valid(self, ct):
		payload = {"option": "unpad", "ct": ct.hex()}
		return self.send_json(payload)['result']

def main():
	io = remote("socket.cryptohack.org", 13421)
	io.recvline()
	io.sendline(dumps({"option": "encrypt"}).encode())
	data = bytes.fromhex(loads(io.recvline().strip().decode())["ct"])
	iv, ciphertext = data[:16], data[16:]

	oracle = Oracle(io)

	password = crack_cbc_padding_oracle(
		oracle=oracle,
		ciphertext=ciphertext,
		iv=iv,
		charset=b"0123456789abcdef"
	).decode()
	io.sendline(dumps({"option": "check", "message": password}).encode())
	flag = io.recvline().strip().decode()
	print(flag)

if __name__ == '__main__':
	main()

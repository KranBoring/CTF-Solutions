from CTF_Crypto_Attack.Symmetric import forge_cbc_padding_oracle
from CTF_Crypto_Attack.Util import BaseSocketOracle
from json import loads, dumps
from pwn import remote

class Oracle(BaseSocketOracle):
	def check_batch(self, cts):
		format = lambda p: dumps({"ciphertext": p.hex()}, separators=(",", ":")).encode()
		self.pipeline_send(cts, format_func=format)
		results = []
		for _ in range(len(cts)):
			res = loads(self.io.recvline().strip().decode())['good_pad']
			results.append(res)
		return results
	def is_padding_valid(self, ct):
		payload = {"ciphertext": ct.hex()}
		return self.send_json(payload)['good_pad']

def main():
	admin_token = '","user_id":"0656d38b8cb0b41b82ecc9859cb7c03e53c7c6610bdce9ea14d30d1a33c80204"}'.encode()

	io = remote("socket.cryptohack.org",13437)
	C_token = bytes.fromhex(loads(io.recvline().strip().decode())['token'])[:16]
	oracle = Oracle(io)
	payload = forge_cbc_padding_oracle(
		oracle=oracle,
		desired_plaintext=admin_token,
		auto_pad=True,
		batch_size=12
	)
	final_payload = C_token + payload
	payload_json = dumps({"ciphertext":final_payload.hex()}).encode()
	io.sendline(payload_json)
	flag = io.recvline().strip().decode()
	print(flag)

if __name__ == '__main__':
	main()

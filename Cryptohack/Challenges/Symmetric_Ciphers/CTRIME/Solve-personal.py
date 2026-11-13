import requests
from requests.adapters import HTTPAdapter
from CTF_Crypto_Attack.Symmetric import compression_oracle

class Oracle:
	def __init__(self, url):
		self.s = requests.session()
		self.s.mount("https://",HTTPAdapter(pool_connections=256, pool_maxsize=256))
		self.url = url
	def get_length(self, plaintext):
		return len(bytes.fromhex(self.s.get(f"{self.url}{plaintext.hex()}/").json()['ciphertext']))

def main():
	oracle = Oracle("https://aes.cryptohack.org/ctrime/encrypt/")
	flag = compression_oracle(
		oracle=oracle,
		known_prefix=b"crypto{",
		suffix=b"}",
		max_workers=256
	)
	print(flag)

if __name__ == '__main__':
	main()

#-------------------------------------------------------------------------------------------------------------#
from CTF_Crypto_Attack.Util import BaseHttpOracle
from CTF_Crypto_Attack.Symmetric import compression_oracle

class Oracle(BaseHttpOracle):
	def get_length(self, plaintext):
		return len(bytes.fromhex(self.get_json(plaintext.hex())['ciphertext']))

def main():
	oracle = Oracle("https://aes.cryptohack.org/ctrime/encrypt/", 256)
	flag = compression_oracle(
		oracle=oracle,
		known_prefix=b"crypto{",
		suffix=b"}",
		max_workers=256
	)
	print(flag)

if __name__ == '__main__':
	main()
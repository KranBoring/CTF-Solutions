#--------------------------------------------------------------------------------------------------#
from CTF_Crypto_Attack.Util import BaseHttpOracle
from CTF_Crypto_Attack.Symmetric import ecb_oracle
from time import time

class Oracle(BaseHttpOracle):
	def encrypt(self, plaintext):
		res = self.get_json(plaintext.hex())
		return bytes.fromhex(res['ciphertext'])

def main() -> None:
	oracle = Oracle("https://aes.cryptohack.org/ecb_oracle/encrypt/", 256)
	flag = ecb_oracle(
		oracle=oracle,
		known_prefix=b"crypto{",
		batch_mode=True,
		max_workers=256
	)
	print(flag)
if __name__ == '__main__':
	start = time()
	main()
	print(f"Thời gian chạy: {time() - start}")
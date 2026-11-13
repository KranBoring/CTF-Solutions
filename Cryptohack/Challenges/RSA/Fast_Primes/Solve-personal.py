#!/usr/bin/env python3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from CTF_Crypto_Attack.RSA import roca_attack


def main():
	key_data = RSA.importKey(open("key.pem").read())
	ciphertext = bytes.fromhex(open("ciphertext.txt").read().strip())

	p, q = roca_attack(key_data.n, key_data.e)

	d = pow(key_data.e, -1, (p - 1) * (q - 1))
	priv_key = RSA.construct((key_data.n, key_data.e, d))
	flag = PKCS1_OAEP.new(priv_key).decrypt(ciphertext)
	print(f"\n[+] FLAG: {flag.decode()}")
if __name__ == "__main__":
	main()
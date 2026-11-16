from CTF_Crypto_Attack.Util import parse_csr

info = parse_csr("readmycert.csr")
print(info['subject']['commonName'])
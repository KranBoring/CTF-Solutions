from Crypto.PublicKey import RSA
import hashlib

with open("transparency_afff0345c6f99bf80eab5895458d8eab.pem","r") as f:
    key = RSA.importKey(f.read())
print(key.public_key())
der = key.exportKey(format = 'DER')
hash256 = hashlib.sha256(der)
print(hash256.hexdigest())
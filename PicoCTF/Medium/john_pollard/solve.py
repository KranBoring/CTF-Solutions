from Crypto.PublicKey import RSA

with open("cert") as f:
    data = RSA.importKey(f.read())
N = data.n
e = data.e


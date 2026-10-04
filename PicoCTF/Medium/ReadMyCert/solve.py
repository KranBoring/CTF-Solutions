from Crypto.PublicKey import RSA
import subprocess

command = "openssl req -in readmycert.csr -noout -pubkey -out pubkey.pem"
shell = subprocess.run(command)
with open("pubkey.pem") as f:
    data = RSA.importKey(f.read())

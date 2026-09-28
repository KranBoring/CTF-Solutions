import json
import base64
from Crypto.Cipher import ChaCha20
with open("output.txt","r") as f:
    data = json.load(f)
cipher = ChaCha20.new(key = data['key'].encode(), nonce = base64.b64decode(data['nonce']))
print(
    cipher.decrypt(base64.b64decode(data['ciphertext']))
)


import requests
from PIL import Image
import io
from pwn import xor

url = "https://aes.cryptohack.org/bean_counter/encrypt/"
s = requests.session()

ciphertext = bytes.fromhex(s.get(f"{url}").json()["encrypted"])
know_bytes = open("apple.png","rb").read(16)

value = xor(ciphertext[:16], know_bytes)
png = xor(ciphertext, value)

img = Image.open(io.BytesIO(png))
img.show()
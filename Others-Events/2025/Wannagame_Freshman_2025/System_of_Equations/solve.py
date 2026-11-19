# %%
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from sage.all import PolynomialRing, QQ, ZZ, ideal

iv = b"\x8d\r\x19\xbc\xfd\x84\x13N,\xf85\xdb\xd3\x92i\x93"
ciphertext = b"\xe9\xa2\x8c\x8b\xc3\xb4\x88\xe2\xbb\x96\xc6\xac`\x1c}\xd1\xca\xc1ZB\xf1@\x01\x92\xca\xc4Z[\x96o\xdeFv\xdf\r\x13u+\x89\xac3\xa3\xc9X\xfb\x07u\x1bO\x9c\xb0\xbdN\xa4\xb6\xca&T\xabmx\xdb\xae\xc2"

R = PolynomialRing(QQ, names="x,y,z", order="lex")
x, y, z = R.gens()

q1 = x**2 + 2 * x * y - 8 - (4 * z**2 + 4 * y - 8 * z)
q2 = x**5 + y**3 + z**4 - 10823714993004958804353333960725385073542379465721
q3 = (
    8864612849141 * x**2
    + 8864612849141 * y
    + 17729225698282 * z
    - 205022233466935232483321764396
)

I = R.ideal([q1, q2, q3])
for sol in I.variety(ZZ):
	print(sol)
	vx, vy, vz = int(sol[x]), int(sol[y]), int(sol[z])
	secret = (str(vx**10) + str(vy**10) + str(vz**10)).encode()
	key = hashlib.sha256(secret).digest()
	try:
		flag = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext), 16)
		print(flag.decode())
	except ValueError:
		pass
# %%

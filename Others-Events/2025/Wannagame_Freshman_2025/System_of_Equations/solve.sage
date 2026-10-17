from sage.all import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib


iv = b'\x8d\r\x19\xbc\xfd\x84\x13N,\xf85\xdb\xd3\x92i\x93'
ciphertext = b'\xe9\xa2\x8c\x8b\xc3\xb4\x88\xe2\xbb\x96\xc6\xac`\x1c}\xd1\xca\xc1ZB\xf1@\x01\x92\xca\xc4Z[\x96o\xdeFv\xdf\r\x13u+\x89\xac3\xa3\xc9X\xfb\x07u\x1bO\x9c\xb0\xbdN\xa4\xb6\xca&T\xabmx\xdb\xae\xc2'

x,y,z = var('x,y,z')

q1 = (x**2 + 2*x*y - 8 == 4*z**2 + 4*y - 8*z)
q2 = (x**5 + y**3 == 10823714993004958804353333960725385073542379465721 - z**4)
q3 = (8864612849141*x**2 + 8864612849141*y + 17729225698282*z == 205022233466935232483321764396)

#print(list(solve([q1,q2,q3],x,y,z)))

a = 33131538
b = 22029258543363862
c = 604095676625
secret = (str(a**10) + str(b**10) + str(c**10)).encode()
key = hashlib.sha256(secret).digest()

flag = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext),16)
print(flag)
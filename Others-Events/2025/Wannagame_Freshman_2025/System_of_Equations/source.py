from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os

FLAG = b'W1{???}'

x = int(input("Nhap x nguyen: "))
y = int(input("Nhap y nguyen: "))
z = int(input("Nhap z nguyen: "))

assert x**2 + 2*x*y - 8 == 4*z**2 + 4*y - 8*z
assert x**5 + y**3 == 10823714993004958804353333960725385073542379465721 - z**4 
assert 8864612849141*x**2 + 8864612849141*y + 17729225698282*z == 205022233466935232483321764396

mode = str(input("Nhap phuong thuc (encrypt hoac decrypt): "))

secret = (str(x**10) + str(y**10) + str(z**10)).encode()
key = hashlib.sha256(secret).digest()

if mode == "encrypt":
    iv = os.urandom(16)
    c = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(FLAG, 16))

    print(f'iv = {iv}')
    print(f'ciphertext = {c}')
    
elif mode == "decrypt":
    iv = b'\x8d\r\x19\xbc\xfd\x84\x13N,\xf85\xdb\xd3\x92i\x93'
    ciphertext = b'\xe9\xa2\x8c\x8b\xc3\xb4\x88\xe2\xbb\x96\xc6\xac`\x1c}\xd1\xca\xc1ZB\xf1@\x01\x92\xca\xc4Z[\x96o\xdeFv\xdf\r\x13u+\x89\xac3\xa3\xc9X\xfb\x07u\x1bO\x9c\xb0\xbdN\xa4\xb6\xca&T\xabmx\xdb\xae\xc2'
    
    FLAG = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext), 16)
    print(FLAG.decode())
    
else:
    exit(1)
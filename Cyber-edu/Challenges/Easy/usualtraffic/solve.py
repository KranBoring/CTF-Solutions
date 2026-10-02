import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def AES_decrypt(ciphertext):
    ciphertext = base64.b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)

iv = bytes.fromhex("8BF46C25D9BAD98ED8EAE6C1F7AD2D04")
key = bytes.fromhex("74C95604043427F0BEE1D0E16BFA53AFD537F736AD0073C4CC4E1CCB3A82B5DC")

secret1 = "KQ6R50gkQLYCkY90yIBDHDznHRUyMaTijWmHO30UXjwftOMIGgZJhKh2xli7Sqln"
secret251 = "uWyYTCYqBTy9afI69to3eK0ScCA3SlPDEzBsWBnR9D8Ro7aIOqihGMPXwu/Z+HLn"

print(AES_decrypt(secret1) + AES_decrypt(secret251))




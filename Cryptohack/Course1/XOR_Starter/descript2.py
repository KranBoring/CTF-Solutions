from pwn import *
plaintext = "label"
key = 13
print(xor(plaintext,key))
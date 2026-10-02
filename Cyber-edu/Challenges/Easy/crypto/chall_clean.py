#!/usr/bin/python 
import textwrap
import os,binascii,hashlib

secret = 'secret'

def rotl(num, bits = 64):
    bit = num & (1 << (bits-1))
    num <<= 1
    if(bit):
        num |= 1
    num &= (2**bits-1)

    return num

def rotr(num, bits = 64):
    num &= (2**bits-1)
    bit = num & 1
    num >>= 1
    if(bit):
        num |= (1 << (bits-1))

    return num



def encrypt(data, key): 
	encrypted = []
	a,b,c= (int(key[i:i+8], 16) for i in range(0, len(key), 8))

	for d in data: 
		d = (ord(d) - (a & 0xff)) ^ (b & 0xff) ^ (c & 0xff)
		d = d & 0xff
		encrypted.append(chr(d))
	
		a = rotr(a)
		b = rotl(b)
		c = rotl(c)

		print(a, b, c)

	return hashlib.sha1(data.encode()).hexdigest() + "".join(encrypted).encode('hex')

key = binascii.b2a_hex(os.urandom(12))
print(key) 
print(encrypt(secret, key))

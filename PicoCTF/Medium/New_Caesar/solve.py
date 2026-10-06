import string

LOWERCASE_OFFSET = ord("a")
ALPHABETb16 = string.ascii_lowercase[:16]

def shift(c, k):
	t1 = ord(c) - LOWERCASE_OFFSET
	t2 = ord(k) - LOWERCASE_OFFSET
	return ALPHABETb16[(t1 - t2) % len(ALPHABETb16)]

def b16_decode(cipher):
    dec = ""
    for i in range(0, len(cipher), 2):
        i1 = ALPHABETb16.index(cipher[i])
        i2 = ALPHABETb16.index(cipher[i+1])
        index = (i1 << 4) + i2
        dec += chr(index)
    return dec

ciphertext = "cbdabldadbplblcnpfpnpapapecpcn"
for i in range(16):
    b16 = ""
    for c in ciphertext:
        b16 += shift(c, chr(i + LOWERCASE_OFFSET))
    flag = b16_decode(b16)
    print(f"{i}. {flag}")
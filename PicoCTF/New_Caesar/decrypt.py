import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

def b16_decode(cipher):
    dec = ""
    for i in range(0,len(cipher),2):
        binary = "{0:04b}".format(ALPHABET.index(cipher[i])) + "{0:04b}".format(ALPHABET.index(cipher[i+1]))
        dec += chr(int(binary,2))
    return dec
#
def shift(c, k):
	t1 = ord(c) - LOWERCASE_OFFSET
	t2 = ord(k) - LOWERCASE_OFFSET
	return ALPHABET[(t1 + t2) % len(ALPHABET)]
#
encflag = "fegdeogdgecoeocgcgchcfcffccfca"
for key in ALPHABET:
    dec = ""
    for c in encflag:
        dec += shift(c,key)
    b16 = b16_decode(dec)
    print(b16,":",key)
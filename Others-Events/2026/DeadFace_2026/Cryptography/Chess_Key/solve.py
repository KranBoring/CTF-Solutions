import string

chesskey = {
    'a':" TNHDZXJA",
    'b':" ZSMGCLBI",
    'c':" DYRLNCKW",
    'd':" HCXPDMBY",
    'e':" JGREOKFA",
    'f':" LTFQWQJE",
    'g':" VGSFBVPI",
    'h':" HUKIEAUO"
}
data = open("MagnusCarlsen.pgn").read().strip().split(' ')
pgn_malnus = []
for i in range(len(data)):
    if data[i][-1] == '.' and data[i + 1] != "O-O-O":
        if data[i + 1][-1] != '+':
            pgn_malnus.append(data[i + 1])
        else:
            pgn_malnus.append(data[i + 1][:-1])
pgn_malnus.pop()

def get_char(square):
    col,row = square[-2], square[-1]
    return chesskey[col][int(row)]

def recover_key(pgn):
    key = ''.join([get_char(step) for step in pgn])
    return key

def Vigenere_decode(ciphertext, key):
    key_index = 0
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            c = ord(char) - base
            k = ord(key[key_index]) - ord('A')
            p = chr((c - k) % 26 + base)
            plaintext += p
            key_index += 1
        else:
            plaintext += char
    return plaintext

key = recover_key(pgn_malnus)
ciphertext = "nZ3ipU8_yy3p5_hvyKi0"
plaintext = Vigenere_decode(ciphertext, key)
print(plaintext)

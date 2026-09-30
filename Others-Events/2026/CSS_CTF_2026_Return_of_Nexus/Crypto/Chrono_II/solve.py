import json

def shifted(c, step):
    global nott
    if c.isalpha():
        return chr((ord(c) - ord('A') - step) % 26 + ord('A') if c.isupper() else (ord(c) - ord('a') - step) % 26 + ord('a'))
    elif c.isnumeric():
        return chr((ord(c) - ord('0') - step) % 10 + ord('0'))
    else:
        nott += 1
        return c 

with open("chrono-ii-capture.json","r") as f:
    json_cipher = json.load(f)
K = []
for i in json_cipher:
    K.append((ord(i["ciphertext"][0]) - ord('C')) % 26)
nott = 0
ciphertext = json_cipher[0]["ciphertext"]
flag = []
for i in range(len(ciphertext)):
    flag.append(shifted(ciphertext[i],K[((i-nott)*43) % 77]))
print(''.join(flag))
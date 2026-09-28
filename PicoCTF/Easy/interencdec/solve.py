import base64

def rotI(text, rot):
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            c = ord(char) - base
            p = (c + rot) % 26 + base
            result.append(chr(p))
        else:
            result.append(char)
    return "".join(result)

with open("enc_flag","r") as f:
    flag = f.read()

flag = base64.b64decode((base64.b64decode(flag).decode()).split('\'')[1]).decode()
for i in range(26):
    if "academy{" in rotI(flag, i):
        print(rotI(flag, i))

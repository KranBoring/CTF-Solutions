import json

def check_shift(flag, text):
    result = []
    for a,b in zip(flag, text):
        result.append((ord(a) - ord(b)) % 26)
    return result
with open("chrono-ii-capture.json","r") as f:
    data = json.load(f)
c = -1
for i in data:
    c += 1
    print(c,'. ',check_shift(i['ciphertext'][:6],"CSSCTF"))
enc = "abcdefghijklmnopqrstuvwxyz\n_"
dec = "sprgwhkqojzldcuvyemnbtiafx\n_"
with open("public/flag.txt") as f:
    cipher = f.read()
flag = ""
for c in cipher:
    index = enc.index(c)
    flag += dec[index]
print(flag)
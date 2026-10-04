with open("encrypted.txt") as f:
    cipher = f.read()
flag = ""
base = ord('a')
for i in cipher:
    flag += i if not i.isalpha() else chr((base - ord(i) - 1) % 26 + base)
print(flag)
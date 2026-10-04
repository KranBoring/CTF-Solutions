list_alphadigist = "ABCDEFGHIJKLMNOPQRSTUQWXYZ0123456789_"
with open("message.txt") as f:
    cipher = [int(i) for i in f.read().strip().split(' ')]
flag = ""
for i in cipher:
    flag += list_alphadigist[i % 37]
print(flag)
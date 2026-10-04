# Part 1
lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

code = ""

with open("ciphertext") as f:
    ciphertext = f.read()
for i in range(len(ciphertext)-1, -1, -1):
    index = 0
    for c in ciphertext[i::-1]:
        index += lookup2.index(c) 
        index %= 40
    code += lookup1[index]
#print(code[::-1])

# Part 2
recode = code[::-1]
b = 1/1
pre = ""
for i in range(len(code)):
    if i == b*b*b:
        pre += recode[i]
        b += 1 / 1
print("academy{"+pre+"}")

encalpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
decalpha = "HCRSNBPMD.ONTIF.YC..ELAG.U"
with open("message.txt") as f:
    data = f.read()
decryptdata = ""
for char in data:
    if char.isalpha():
        index = encalpha.index(char.upper())
        decryptdata += decalpha[index] if char.isupper() else decalpha[index].lower()
    else:
        decryptdata += char
print(decryptdata.split('s')[-1])

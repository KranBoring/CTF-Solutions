plaintext = "label"
key = 13
cipher = ""

for i in plaintext:
    cipher += chr(ord(i)^key)
print(cipher)

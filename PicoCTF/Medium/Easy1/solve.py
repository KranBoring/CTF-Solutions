def shifted(char,chark):
    return (chr((ord(char)-ord(chark)) % 26 + ord('A')))

key = "SOLVECRYPTO"
ciphertext = "UFJKXQZQUNB"

flag = ""
for i in range(len(ciphertext)):
    flag += shifted(ciphertext[i], key[i])
print("academy{"+f"{flag}"+"}")

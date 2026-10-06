def caesar(char, step):
    return (char if not char.isalpha() else chr((ord(char) - ord('a') + step) % 26 + ord('a')))

with open("data.enc") as f:
    ciphertext = f.read()

ciphertext = ciphertext.split('{')
for i in range(26):
    flag = ""
    for c in ciphertext[1]:
        flag += caesar(c, i)
    print(f"{ciphertext[0]}{chr(ord('{'))}{flag}")
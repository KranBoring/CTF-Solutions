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
with open("values.txt","r") as f:
    flag = f.read()

for i in range(26):
    result = rotI(flag ,i)
    if "academy{" in result:
        print(result)
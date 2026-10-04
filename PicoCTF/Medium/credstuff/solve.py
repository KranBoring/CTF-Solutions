cipher = "npnqrzl{P7e1S_54I35_71Z3}"
def shifted(char, step):
    if char.isalpha():
        base = ord('A') if char.isupper() else ord('a')
        return chr((ord(char) - base + step) % 26 + base)
    else:
        return char
for i in range(26):
    flag = ""
    for c in cipher:
        flag += shifted(c, i)
    if "academy{" in flag:
        print(flag)
        break
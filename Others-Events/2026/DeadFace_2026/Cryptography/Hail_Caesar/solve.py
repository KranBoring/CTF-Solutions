message = "Zl qbt'f anzr vf Srgpv​"
for i in range(26):
    new_messgae = ""
    for char in message:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            new_messgae += chr((ord(char) - base + i) % 26 + base)
        else:
            new_messgae += char
    print(new_messgae)
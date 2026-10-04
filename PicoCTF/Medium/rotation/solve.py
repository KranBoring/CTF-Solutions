def shifted(char, step):
    return (
        str(char) if not char.isalpha() else chr((ord(char) - ord('a') + step) % 26 + ord('a'))
    )

with open("encrypted.txt") as f:
    ciphertext = f.read().strip()
for i in range(26):
    flag = "".join([shifted(char ,i) for char in ciphertext])
    if "academy{" in flag:
        print(flag)
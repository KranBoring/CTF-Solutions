def caesar_solve(text, key):
    result = []
    key_len = len(key)
    key_idx = 0
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            c = ord(char) - base
            k = ord(key[key_idx % key_len]) - ord('A')
            p = (c - k) % 26
            result.append(chr(p+base))
            key_idx += 1
        else:
            result.append(char)
    return "".join(result)
with open("cipher.txt") as f:
    cipher = f.read().strip()
print(caesar_solve(cipher, "CYLAB"))
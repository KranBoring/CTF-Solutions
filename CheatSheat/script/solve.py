def solve(text, key):
    result = []
    key = key.upper()
    leng = len(key)
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
print(solve("rgnoDVD{O0NU_WQ3_G1G3O3T3_A1AH3S_cc82272b}", "CYLAB"))
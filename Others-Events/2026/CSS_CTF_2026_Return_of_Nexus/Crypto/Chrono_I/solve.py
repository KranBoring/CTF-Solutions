def caesar_solve(text, key = "20260921143507"):
    result = []
    key_len = len(key)
    key_idx = 0
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            c = ord(char) - base
            k = int(key[key_idx % key_len])

            p = (c - k) % 26
            result.append(chr(p+base))
            key_idx += 1
        else:
            result.append(char)
    return "".join(result)
print(caesar_solve("ESUITO{gwfvb_xejqnf_nimgt_b_whhrlv}"))

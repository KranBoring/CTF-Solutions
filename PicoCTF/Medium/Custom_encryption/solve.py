a = 95
b = 31
p = 97
g = 31
cipher = [134352, 343344, 238848, 1194240, 0, 1298736, 1059888, 1134528, 1059888, 626976, 0, 1239024, 313488, 74640, 1015104, 0, 328416, 1283808, 14928, 925536, 358272, 403056, 89568, 89568, 253776, 89568, 388128, 179136, 373200, 343344, 253776, 74640, 89568, 0]

def decrypt(cipher, key):
    plaintext = ""
    for i in cipher:
       plaintext += chr(i // (key * 311))
    return plaintext

def dynamic_xor_decrypt(cipher, text_key):
    plaintext = ""
    key_length = len(text_key)
    for i, char in enumerate(cipher):
        key_char = text_key[i % key_length]
        decrypted_char = chr(ord(char) ^ ord(key_char))
        plaintext += decrypted_char
    return plaintext[::-1]

shared_key = pow(g, a*b, p)
semi_cipher = decrypt(cipher, shared_key)
flag = dynamic_xor_decrypt(semi_cipher, "trudeau")
print(flag)


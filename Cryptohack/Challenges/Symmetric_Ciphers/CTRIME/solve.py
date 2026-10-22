import requests
import string

url = "https://aes.cryptohack.org/ctrime/encrypt/"
s = requests.session()

def encrypt(plaintext, padding):
    payload = padding.hex() + plaintext.encode().hex()
    ciphertext = s.get(f"{url + payload}/").json()["ciphertext"]
    return ciphertext

alphabet = string.ascii_letters + string.digits + "{" + "}" + "_"

def find_next_char(cur_flag):
    for pad in range(16):
        padding = pad * b"\x00"
        length = {}
        for char in alphabet:
            test_payload = cur_flag + char
            length[char] = len(encrypt(test_payload, padding))
        min_len = min(length.values())
        max_len = max(length.values())
        if min_len < max_len:
            next_char = [char for char,len in length.items() if len == min_len]
            return next_char
    return []

def dfs(cur_flag):
    print(cur_flag)
    if cur_flag.endswith("}"):
        return cur_flag
    next_char = find_next_char(cur_flag)
    for char in next_char:
        result = dfs(cur_flag + char)
        if result is not None:
            return result
    return None

flag = "crypto{"
flag = dfs(flag)
print(f"Flag: {flag}")
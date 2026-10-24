import string
from pwn import xor

english_alphabet = set((string.ascii_letters + " .',-?").encode())
flag_alphabet = set((string.ascii_lowercase + string.digits + "_{}").encode())

def find_next_char(cur_flag):
    list_char = []
    for char in flag_alphabet:
        result = []
        for cipher in ciphertext:
            if len(cipher) >= len(cur_flag) + 1 and len(flag_ciphertext) > len(cur_flag):
                result.append(cipher[len(cur_flag)] ^ flag_ciphertext[len(cur_flag)] ^ char)
        if all(char in english_alphabet for char in result) and result != []:
            list_char.append(char)
    return list_char

def dfs(cur_flag):
    if cur_flag.endswith(b'}'):
        flags.append(cur_flag)
        return
    next_char = find_next_char(cur_flag)
    for char in next_char:
        result = dfs(cur_flag + bytes([char]))
        if result is not None:
            flags.append(cur_flag)
    return None

ciphertext = []
with open("ciphertext.txt",'r') as f:
    for i in range(22):
        ciphertext.append(bytes.fromhex(f.readline().strip()))
    flag_ciphertext = bytes.fromhex(f.readline().strip())
    ciphertext.remove(flag_ciphertext)

flags = []
flag = b'crypto{'
dfs(flag)

for flag in flags:
    print(f"Flag: {flag}")
    for cipher in ciphertext:
        print(xor(xor(cipher, flag_ciphertext), flag))
    space = input()


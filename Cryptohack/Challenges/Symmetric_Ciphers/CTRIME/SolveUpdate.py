import requests
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor
import string
from time import time

alphabet = string.ascii_letters + string.digits + "{" + "}" + "_"
lenght_alphabet = len(alphabet)

url = "https://aes.cryptohack.org/ctrime/encrypt/"
s = requests.session()
s.mount("https://", HTTPAdapter(pool_connections=lenght_alphabet, pool_maxsize=lenght_alphabet))

def encrypt(plaintext, padding):
    payload = padding.hex() + plaintext.encode().hex()
    ciphertext = s.get(f"{url + payload}/").json()["ciphertext"]
    return len(ciphertext)

def find_next_char(cur_flag):
    for pad in range(16):
        padding = pad * b"\x00"
        length = []
        test_payloads = [cur_flag + char for char in alphabet]
        with ThreadPoolExecutor(max_workers=lenght_alphabet) as f:
            length = list(f.map(encrypt, test_payloads, [padding] * lenght_alphabet))
        min_len = min(length)
        max_len = max(length)
        if min_len < max_len:
            next_char = [alphabet[length.index(len)] for len in length if len == min_len]
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

if __name__ == '__main__':

    start = time()

    flag = "crypto{"
    flag = dfs(flag)
    print(f"Flag: {flag}")

    end = time()
    print(f"Thời gian chạy: {end - start}")
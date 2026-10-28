import requests
from requests.adapters import HTTPAdapter
from json import dumps
from concurrent.futures import ThreadPoolExecutor
from pwn import xor
from time import time
from Crypto.Util.Padding import unpad
import string

url = "https://aes.cryptohack.org/paper_plane/"
s = requests.session()
s.mount('https://', HTTPAdapter(pool_connections=100, pool_maxsize=100))

def b(text):
    return bytes.fromhex(text)

def get_cipher_flag():
    data = s.get(f"{url}encrypt_flag/").json()
    return b(data['ciphertext']), b(data['c0']), b(data['m0'])

def send_ciphertext(cipher, m0, c0):
    cipher, m0, c0 = cipher.hex(), m0.hex(), c0.hex()
    data = s.get(f"{url}send_msg/{cipher}/{m0}/{c0}/").json()
    return 'msg' in data

def xorn(m, number):
    return bytes([]) if m == b'' else bytes([a ^ number for a in m])

if __name__ == '__main__':
    start = time()

    flag_alphabet = (string.ascii_letters + string.digits + '_{}').encode() + bytes(range(1,17))
    length_know_flag = len(flag_alphabet)
    ciphertext, c0, m0 = get_cipher_flag()
    block_ciphertext = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]
    full_block = [c0] + block_ciphertext
    prev_m = m0
    prev_c = c0
    flag = b''
    for index in range(len(block_ciphertext)):
        know_bytes = b''
        prev_block = full_block[index]
        m0_payloads = [prev_m] * length_know_flag
        for count in range(16):
            pos = 15 - count
            list_bytes = [c ^ prev_block[pos] ^ (count + 1) for c in flag_alphabet]
            c0_payloads = [b'\x00' * (16 - count - 1) + bytes([i]) + xorn(know_bytes, count + 1) for i in list_bytes]
            with ThreadPoolExecutor(max_workers=length_know_flag) as f:
                response_payloads = list(f.map(send_ciphertext, [block_ciphertext[index]] * length_know_flag, m0_payloads, c0_payloads))
            know_bytes = bytes([list_bytes[response_payloads.index(True)] ^ (count + 1)]) + know_bytes
        plain = xor(know_bytes, prev_c)
        prev_m = plain
        prev_c = block_ciphertext[index]
        flag += plain
    flag = unpad(flag, 16).decode()
    print(flag)

    end = time()
    print(f"Thời gian chạy: {(end - start):.2f}")



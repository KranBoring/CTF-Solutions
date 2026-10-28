import requests
from json import dumps
from concurrent.futures import ThreadPoolExecutor
from pwn import xor
from time import time
from Crypto.Util.Padding import unpad

url = "https://aes.cryptohack.org/paper_plane/"

def b(text):
    return bytes.fromhex(text)

def get_cipher_flag():
    data = requests.get(f"{url}encrypt_flag/").json()
    return b(data['ciphertext']), b(data['c0']), b(data['m0'])

def send_ciphertext(cipher, m0, c0):
    cipher, m0, c0 = cipher.hex(), m0.hex(), c0.hex()
    data = requests.get(f"{url}send_msg/{cipher}/{m0}/{c0}/").json()
    return 'msg' in data

def xorn(m, number):
    return bytes([]) if m == b'' else bytes([a ^ number for a in m])

if __name__ == '__main__':
    start = time()

    ciphertext, c0, m0 = get_cipher_flag()
    block_ciphertext = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]
    prev_m = m0
    prev_c = c0
    flag = b''
    for index in range(len(block_ciphertext)):
        know_bytes = b''
        m0_payloads = [prev_m] * 256
        for count in range(16):
            c0_payloads = [b'\x00' * (16 - count - 1) + bytes([i]) + xorn(know_bytes, count + 1) for i in range(256)]
            with ThreadPoolExecutor(max_workers=100) as f:
                response_payloads = list(f.map(send_ciphertext, [block_ciphertext[index]] * 256, m0_payloads, c0_payloads))
            know_bytes = bytes([response_payloads.index(True) ^ (count + 1)]) + know_bytes
        plain = xor(know_bytes, prev_c)
        prev_m = plain
        prev_c = block_ciphertext[index]
        flag += plain
    flag = unpad(flag, 16).decode()
    print(flag)

    end = time()
    print(f"Thời gian chạy: {(end - start):.2f}")



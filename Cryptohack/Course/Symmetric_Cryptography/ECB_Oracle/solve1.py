import requests
import time
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor

start = time.time()

url = "https://aes.cryptohack.org/ecb_oracle/encrypt/"
hex_string = lambda s: s[2:]
list_print = list(map(hex_string ,map(hex ,map(ord ," etaoinsrhldcumwfgypbvkjxqzETAOINSRHLDCUMWFGYPBVKJXQZ9876543210,.?!-^\":;'&_%@=*+$#\\/][}{><|^`~"))))
flag = "crypto{"
len_flag = 26

s = requests.session()
s.mount('https://', HTTPAdapter(pool_connections=256, pool_maxsize=256))

def big_payloads(round, know_flag):
    payloads = []
    payload = ""
    for i,charP in enumerate(list_print):
        payload += (32 - round) * "00" + ''.join([str(hex(ord(char)))[2:] for char in know_flag]) + charP
        if (i + 1) % 28 == 0:
            payloads.append(payload)
            payload = ""
    payloads.append(payload)
    return payloads

def flag_check(tests, ciphertext, count):
    global flag
    for test in tests:
        if test == ciphertext:
            flag += chr(int(list_print[tests.index(test) + count], 16))
            print(flag)
            return True
    return False

def send_payload(payload):
    data = bytes.fromhex(s.get(f"{url}{payload}/").json()["ciphertext"])
    return [data[i :i + 32] for i in range(0, 28 * 32, 32)]

for round in range(len(flag) + 1,len_flag):
    payload = (32 - round) * "00"
    ciphertext = bytes.fromhex(s.get(f"{url}{payload}/").json()["ciphertext"])
    ciphertext = ciphertext[:32]

    new_payloads = big_payloads(round, flag)

    count = 0
    '''for payload in new_payloads:
        test = send_payload(payload)
        check = flag_check(test, ciphertext, count)
        if check:
            break
        count += 28'''
    with ThreadPoolExecutor(max_workers=256) as f:
        test_payloads = list(f.map(send_payload, new_payloads))
    for test in test_payloads:
        check = flag_check(test, ciphertext, count)
        if check:
            break
        count += 28
    

end = time.time()
print(f"Thoi gian thuc thi: {end - start}")
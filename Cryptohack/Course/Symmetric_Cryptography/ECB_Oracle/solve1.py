import requests
import time

start = time.time()

url = "https://aes.cryptohack.org/ecb_oracle/encrypt/"
hex_string = lambda s: s[2:]
list_print = list(map(hex_string ,map(hex ,map(ord ," etaoinsrhldcumwfgypbvkjxqzETAOINSRHLDCUMWFGYPBVKJXQZ9876543210,.?!-^\":;'&_%@=*+$#\\/][}{><|^`~"))))
flag = "crypto{"
len_flag = 26

s = requests.session()

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

for round in range(len(flag) + 1,len_flag):
    payload = (32 - round) * "00"
    ciphertext = bytes.fromhex(s.get(f"{url}{payload}/").json()["ciphertext"])
    ciphertext = ciphertext[:32]

    new_payloads = big_payloads(round, flag)

    count = 0
    for payload in new_payloads:
        test = bytes.fromhex(s.get(f"{url}{payload}/").json()["ciphertext"])
        test = [test[i :i + 32] for i in range(0, 28 * 32, 32)]
        check = flag_check(test, ciphertext, count)
        if check:
            break
        count += 28

end = time.time()
print(f"Thoi gian thuc thi: {end - start}")
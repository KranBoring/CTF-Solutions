import json
import requests
import time

start = time.time()

len_flag = 26
url = "https://aes.cryptohack.org/ecb_oracle/encrypt/"
list_print = [str(hex(i))[2:] for i in range(int("20",16), int("7F",16))]
flag = "crypto{"

for round in range(len(flag) + 1,len_flag):
    payload = (32 - round) * "00"
    ciphertext = bytes.fromhex(json.loads(requests.get(f"{url}{payload}/").text)["ciphertext"])
    ciphertext = ciphertext[:32]
    i = -1
    while True:
        i += 1
        new_payload = (32 - round) * "00" + ''.join([str(hex(ord(char)))[2:] for char in flag]) + list_print[i]
        test = bytes.fromhex(json.loads(requests.get(f"{url}{new_payload}/").text)["ciphertext"])
        test = test[:32]
        if test == ciphertext:
            flag += chr(int(list_print[i], 16))
            print(flag)
            break
    if flag.endswith("}"):
        break

end = time.time()
print(f"Thoi gian thuc thi: {end - start}")
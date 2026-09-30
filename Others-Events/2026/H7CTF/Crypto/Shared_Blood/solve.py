import math
import json
import requests
from Crypto.Util.number import bytes_to_long,long_to_bytes

url = "https://web-0150421386267362.web.h7tex.com"

with open("fleet.txt","w") as f:
    data = requests.get(f"{url}/fleet")
    f.write(data.text)
with open("captured.txt","w") as f:
    data = requests.get(f"{url}/captured")
    f.write(data.text)
with open("fleet.txt","r") as f:
    fleet = json.load(f)
with open("captured.txt","r") as f:
    captured = json.load(f)

for i in fleet['devices']:
    if i['serial'] == captured['serial']:
        main_n = int(i['n'])
        main_e = int(captured['e'])
        main_cipher = int(captured['ciphertext'], 16)
for i in fleet['devices']:
    check = math.gcd(main_n, int(i['n']))
    if (check) > 1 and check != main_n:
        q = check
        p = main_n // check
        break
T = (q - 1)*(p - 1)
d = pow(main_e, -1, T)
plaintext = long_to_bytes(pow(main_cipher, d, main_n)).split(b'\x00')[1]

json_data = {
    "token": plaintext.decode()
}
flag = requests.post(f"{url}/admin", json=json_data)

print(flag.status_code)
print(flag.text)

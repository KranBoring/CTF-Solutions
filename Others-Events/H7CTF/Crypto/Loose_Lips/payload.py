import json
import requests

url = "https://web-e4e6c79cd2f58e59.web.h7tex.com"
v1 = {"s": [0, 1, 0, 0, -1, -1, 0, 1]}
v2 = {"s": [0, 0, -1, 1, -1, 1, 1, 0]}

v1_re = requests.post(f"{url}/v1/recover", json=v1)
v2_re = requests.post(f"{url}/v2/recover", json=v2)

print(v1_re.text)
print(v2_re.text)

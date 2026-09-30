import json,requests

url = "https://web-e4e6c79cd2f58e59.web.h7tex.com"
payload = {"values": [1.0,0.0,0.0,0.0]}


with open("enc.txt","w") as f:
    data = requests.post(f"{url}/v1/encrypt", json= payload)
    f.write(data.text)
with open("enc.txt","r") as f:
    enc = json.load(f)
with open("dec.txt","w") as f:
    data = requests.post(f"{url}/v1/decrypt", json={"id":enc["id"]})
    f.write(data.text)
with open("dec.txt","r") as f:
    dec = json.load(f)
print(dec['result'][1])
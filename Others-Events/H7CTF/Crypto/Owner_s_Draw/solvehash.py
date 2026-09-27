import hashpumpy
import requests
import hashlib
import json

url = "https://web-99ade1ce61698c4a.web.h7tex.com"

with open("output.txt","w") as f:
    data = requests.get(f"{url}/sample").json()
    f.write(str(data))
    body = data["body"].encode()
    guest_sig = data['X-Signature'].encode()

admin = b"&role=owner"

for sec_len in range(65):
    admin_sig, admin_body = hashpumpy.hashpump(
        guest_sig.decode(),
        body.decode(),
        admin.decode(),
        sec_len
    )
    header = {
        "X-Signature" : admin_sig,
    }
    response = requests.post(f"{url}/webhook", headers = header, data=admin_body, timeout=10)
    print("secret lenght:",sec_len)
    print("response status:", response.status_code)
    if response.status_code == 200:
        print(response.text)
        break
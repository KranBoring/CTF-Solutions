import json,requests

url = "https://web-907a99606d1accdf.web.h7tex.com"

with open("root.txt","w") as f:
    data = requests.get(f"{url}/root")
    f.write(data.text)
    print(data.text)
    print(data.status_code)
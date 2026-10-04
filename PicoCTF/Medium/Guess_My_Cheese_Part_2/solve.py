import hashlib
from pwn import *

io = remote("chatelaine.cylabacademy.net", 39405)
target_cheese_hash = ""
def payload(payload):
    io.sendline(str(payload).encode())
    print(payload)
def reuntil(text):
    res = io.recvuntil(text.encode())
    print(res.decode())
def readlinehash():
    global target_cheese_hash
    target_cheese_hash = io.recvline().strip().decode()
    print(target_cheese_hash)

reuntil("What would you like to do?")
payload("g")
reuntil("Remember, this is my encrypted cheese:  ")
readlinehash()
reuntil("So...what's my cheese?")
with open("cheese_list.txt", "r") as f:
    cheeses = [line.strip() for line in f if line.strip()]

case_text = {
    "original": lambda s: s,
    "lower": lambda s: s.lower(),
    "upper": lambda s: s.upper(),
}

for cheese in cheeses:
    for case_name, case_func in case_text.items():
        cheese_bytes = case_func(cheese).encode()
        for salt in range(256):
            salt_raw = bytes([salt])
            salt_hex_lower = f"{salt:02x}".encode()
            salt_hex_upper = f"{salt:02X}".encode()

            test_case = [
                cheese_bytes + salt_raw,
                salt_raw + cheese_bytes,
                cheese_bytes + salt_hex_lower,
                cheese_bytes + salt_hex_upper,
                salt_hex_lower + cheese_bytes,
                salt_hex_upper + cheese_bytes
            ]
            for test in test_case:
                hash_value = hashlib.sha256(test).hexdigest()
                if target_cheese_hash == hash_value:
                    payload(cheese)
                    reuntil("Annnnd...what's my salt?")
                    payload(f"{salt:02x}")
                    reuntil("academy{cHeEsYf43fe6b8}")
                    print(f"Cheese: {cheese} (Case name: {case_name})")
                    print(f"Salt: {salt} (Hex: {salt:02x})")
                    print(f"test_case: {test_case.index(test)}")
                    io.interactive()

        

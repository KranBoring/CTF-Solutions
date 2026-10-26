from pwn import *
from json import dumps, loads
import time
from concurrent.futures import ProcessPoolExecutor

def main(count_main):
    host = "socket.cryptohack.org"
    port = 13423
    io = remote(host, port, timeout=60)

    def reline():
        res = io.recvline().strip().decode()
        return res

    def sendl(payload):
        io.sendline(payload.encode())

    def json_unpad(payload):
        return dumps({'option':'unpad','ct': payload.hex()}, separators=(',', ':'))

    def padding_attack(payload, leng):
        try:
            io.send(payload.encode())
            res = []
            for _ in range(leng):
                check = loads(reline())
                res.append(check['result'])
            return res
        except Exception:
            return None

    def xorn(m, number):
        return bytes([]) if m == b'' else bytes([a ^ number for a in m])

    def find_block_message(index):
        nonlocal message
        def check_payload(payload):
            total = 0
            true_count = 0
            for _ in range(7):
                batch = (json_unpad(payload) + '\n') * 10
                try:
                    res = padding_attack(batch, 10)
                except Exception:
                    return None
                true_count += res.count(True)
                total += 10
                rate = true_count / total
                if total == 10 and rate >= 0.8:
                    return False, rate
                if total == 20 and rate >= 0.65:
                    return False, rate
                if total == 40 and rate >= 0.575:
                    return False, rate
            check = true_count <= 32
            return (check, true_count / total)
        
        def dfs(curr_count, index, curr_know_bytes):
            nonlocal message
            if curr_count == 16:
                message += curr_know_bytes
                return True
            pos = 15 - curr_count
            list_bytes = [c ^ prev_block[pos] ^ (curr_count + 1) for c in HEX]
            payloads = [b'\x00' * pos + bytes([i]) + xorn(curr_know_bytes[::-1], curr_count + 1) + block_ciphertext[index] for i in list_bytes]
            checked = {}
            for i in range(16):
                try:
                    check, rate = check_payload(payloads[i])
                except Exception:
                    return None
                if check:
                    print(f"[+] Block {index} - Bytes {curr_count} - i = {i} (rate = {rate})")
                    next_know_bytes = curr_know_bytes + bytes([(curr_count + 1) ^ list_bytes[i]])
                    if dfs(curr_count + 1, index, next_know_bytes):
                        return True
                    print(f"[+] i = {i} chọn sai")
                elif rate <= 0.5:
                    checked = checked | {rate:i}

            if checked:
                minrate = min(checked.keys())
                next_know_bytes = curr_know_bytes + bytes([(curr_count + 1) ^ list_bytes[checked[minrate]]])
                print(f"[+] Chạy dự phòng: i = {checked[minrate]} (rate = {minrate})")
                if dfs(curr_count + 1, index, next_know_bytes):
                    return True
            return None 

        dfs(0, index, b'')
    try:
        reline()
        sendl(dumps({"option":"encrypt"}))
        data = bytes.fromhex(loads(reline())["ct"])
    except Exception:
        return 'Fail to connect'

    iv,ciphertext = data[:16], data[16:]
    block_ciphertext = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]

    full_block = [iv] + block_ciphertext
    HEX = b"1234567890abcdef"

    message = b''
    count_block = 0
    for index in range(len(block_ciphertext) - 1, -1, -1):
        count_block += 1
        prev_block = full_block[index]
        find_block_message(index)
        if len(message) != count_block * 16:
            return "Fail to find message"
    try:
        message = message[::-1]
        message = (xor(message[:16], iv) + xor(message[16:], block_ciphertext[0])).decode()

        last_payload = dumps({'option':'check','message':message})
        sendl(last_payload)
        flag = loads(reline())
    except Exception:
        return "Fail to find message"

    try:
        value = flag["flag"]
    except Exception:
        value = flag["error"]
    return value
    

if __name__ == '__main__':
    start = time.time()
    flag = ""
    count = 0
    with open("logs.txt","w") as f:
        f.write("Bắt đầu logs:\n")
    while True:
        with ProcessPoolExecutor(max_workers=50) as f:
            result = list(f.map(main, range(50)))
        count += 50
        with open("logs.txt","a") as f:
            for res in result:
                f.write(f"#------{res}------#\n")
                print(f"#------{res}------#\n")
        for res in result:
            if 'crypto{' in res:
                flag = res
                break
        if flag != "":
            break
    print(flag)
    print(f"Tổng số tiến trình: {count}")
    end = time.time()
    print(f"Tông thời gian chạy: {(end - start):.2f}")
    with open("logs.txt","a") as f:
        f.write(f"Tông thời gian chạy: {(end - start):.2f}")
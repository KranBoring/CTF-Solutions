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
        know_bytes = b''
        for count in range(16):
            pos = 15 - count
            list_bytes = [c ^ prev_block[pos] ^ (count + 1) for c in HEX]
            payloads = [b'\x00' * pos + bytes([i]) + xorn(know_bytes[::-1], count + 1) + block_ciphertext[index] for i in list_bytes]

            score = [0] * 16
            while (m := max(score)) < 23:
                i = score.index(m)
                batch = (json_unpad(payloads[i])  + '\n') * 10
                res = padding_attack(batch, 10)
                if res is None:
                    return "Fail to find message"
                score[i] += sum([(-1) ** check for check in res])
            know_bytes += bytes([(count + 1) ^ list_bytes[score.index(max(score))]])
        message += know_bytes
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
    with open("logsUp.txt","w") as f:
        f.write("Bắt đầu logs:\n")
    while True:
        with ProcessPoolExecutor(max_workers=10) as f:
            result = list(f.map(main, range(10)))
        count += 10
        with open("logsUp.txt","a") as f:
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
    with open("logslocalhost.txt","a") as f:
        f.write(f"Tổng số tiến trình: {count}")
        #f.write(f"Xác suất chạy đúng mỗi tiến trình là: {(count_flag / 2000):.2f}")
        f.write(f"Tông thời gian chạy: {(end - start):.2f}")

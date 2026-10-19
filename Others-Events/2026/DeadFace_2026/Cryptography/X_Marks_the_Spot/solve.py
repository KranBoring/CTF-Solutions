from pwn import xor

def check(list):
    return [0x20 <= i <= 0x7e for i in list]

hex_string = "02362b2964302c2164372c25202b3337642b226417342127303621641021272c2a2b282b233d7e6420212520222527213f3c2b361b751b263d30771b70301b701b3075297739"
message = bytes.fromhex(hex_string)
for key in range(256):
    new_messgae = xor(message, key)
    if all(check(new_messgae)):
        print(new_messgae.decode())
#!/usr/bin/env python3

import secrets
import signal
import sys

from Crypto.Cipher import DES3
from secret import FLAG, MASK


KEY_SIZE = 24
BLOCK_SIZE = 8
TIMEOUT = 120

BLUE = "\033[38;5;15;48;5;18m"
CYAN = "\033[38;5;51;48;5;18m"
GREY = "\033[38;5;250m"
RESET = "\033[0m"

BANNER = f"""
{BLUE}+------------------------------------------------------------------------------+{RESET}
{BLUE}|                                                                              |{RESET}
{BLUE}|   DDDD   EEEE   SSSS  BBBB                            0.74-3                 |{RESET}
{BLUE}|   D   D  E     S      B   B                                                  |{RESET}
{BLUE}|   D   D  EEEE   SSS   BBBB    OOO   X  X        {CYAN}cryptographic shell{BLUE}          |{RESET}
{BLUE}|   D   D  E         S  B   B  O   O   XX                                      |{RESET}
{BLUE}|   DDDD   EEEE  SSSS   BBBB    OOO   X  X                                     |{RESET}
{BLUE}|                                                                              |{RESET}
{BLUE}+------------------------------------------------------------------------------+{RESET}

{GREY}Z:\\>MOUNT C C:\\DESBOX{RESET}
Drive C is mounted as local directory C:\\DESBOX

{GREY}Z:\\>C:{RESET}
{GREY}C:\\>DIR{RESET}
"""

DIRECTORY = r"""
 Volume in drive C has no label.
 Volume Serial Number is 1337-BEEF

 Directory of C:\

KEYB     COM        3,584  06-24-26  12:00p
README   TXT          640  06-24-26  12:00p
FLAG     BIN           48  06-24-26  12:00p
        3 file(s)        4,272 bytes
"""

README = r"""
DESBox README.TXT
-----------------
KEYB.COM accepts two different 24-byte 3DES keys, written as hex.

Before a key is loaded, the keyboard controller randomly permutes its bytes
and xors the result with a resident secret table.

Commands: DIR, TYPE README.TXT, KEYB, DOOM, EXIT
"""

PROMPT = r"C:\> "
RNG = secrets.SystemRandom()


def timeout_handler(signum, frame):
    sys.exit(1)


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def permute(a):
    p = list(range(len(a)))
    RNG.shuffle(p)
    return bytes(a[i] for i in p)


def des_bits(a):
    return bytes(x & 0xFE for x in a)


def load_key(user_key):
    key = xor(permute(user_key), MASK)
    return DES3.adjust_key_parity(key)


def effective_bytes(k):
    return [b & 0xFE for b in k]


def is_effective_complement(a, b):
    def complement(k):
        return bytes(x ^ 0xff for x in k)

    return effective_bytes(a) == effective_bytes(complement(b))


def read_keys():
    key_a = bytes.fromhex(input("KEY A> ").strip())
    key_b = bytes.fromhex(input("KEY B> ").strip())

    if len(key_a) != 24 or len(key_b) != 24:
        print("Bad key size.")
        exit()

    if key_a == key_b:
        print("Keyboard layouts must be different.")
        exit()

    if effective_bytes(key_a) == effective_bytes(key_b):
        print("Keyboard layouts are equivalent.")
        exit()

    if sorted(effective_bytes(key_a)) == sorted(effective_bytes(key_b)):
        print("Keyboard layouts use the same scan code multiset.")
        exit()

    if is_effective_complement(key_a, key_b):
        print("Keyboard layouts are too symmetric.")
        exit()

    return load_key(key_a), load_key(key_b)


def run_keyb():
    print("Loading KEYB.COM ...")
    print("Enter two different 24-byte keys as hex.\n")

    key_a, key_b = read_keys()

    print("\nC:\\FLAG.BIN encrypted under Key A:")
    print(DES3.new(key_a, DES3.MODE_ECB).encrypt(FLAG).hex())

    ct = bytes.fromhex(input("\nDebug ciphertext> ").strip())
    if len(ct) == 0 or len(ct) % BLOCK_SIZE != 0:
        print("Bad ciphertext size.")
        sys.exit(1)

    print("Debug output:")
    print(DES3.new(key_b, DES3.MODE_ECB).decrypt(ct).hex())


def type_file(name):
    name = name.upper()
    if name in {"README", "README.TXT"}:
        print(README)
    elif name in {"KEYB", "KEYB.COM"}:
        print("Cannot TYPE binary file.")
    elif name in {"FLAG", "FLAG.BIN"}:
        print("Access denied.")
    else:
        print("File not found.")


def shell():
    print(BANNER)
    print(DIRECTORY)

    while True:
        line = input(PROMPT).strip()
        if not line:
            continue

        cmd, _, arg = line.partition(" ")
        cmd = cmd.upper()
        arg = arg.strip()

        if cmd == "DIR":
            print(DIRECTORY)
        elif cmd == "TYPE":# Ke me
            type_file(arg)
        elif cmd in {"KEYB", "KEYB.COM"}: # focus
            run_keyb()
        elif cmd == "DOOM": # Ke me
            print("This program cannot be run in DESBox mode.")
        elif cmd in {"EXIT", "QUIT"}: # ke me
            return
        else: # ke me
            print("Bad command or file name.")


def main():
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(TIMEOUT)

    assert len(FLAG) % BLOCK_SIZE == 0

    shell()


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt, ValueError):
        sys.exit(1)

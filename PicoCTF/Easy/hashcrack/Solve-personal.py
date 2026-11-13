#!/usr/bin/env python3
import subprocess
def main() -> None:
    cmd = "john --wordlist=rockyou.txt hashfile.txt --format=RAW-MD5".split(' ')
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
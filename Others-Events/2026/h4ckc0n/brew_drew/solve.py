#!/usr/bin/env python3
from CTF_Crypto_Attack.Util import parsers
from Crypto.Util.number import long_to_bytes

def main() -> None:
   data = parsers("logged_convo.txt",multi_value=True)
   drew = data['drew']
   brew = data['brew']
   for name, msg_list in [("brew", brew), ("drew", drew)]:
      for i, val in enumerate(msg_list):
         print(f"=== {name} {i} ===")
         bits = bin(val)[2:].zfill(1751)
         for r in range(103):
            row = bits[r * 17 : (r + 1) * 17]
            print(row.replace("0", " ").replace("1", "#"))

if __name__ == "__main__":
   main()

key = "SOLVECRYPTO"
flag_enc = "UFJKXQZQUNB"

offset = ord('A')
dec = ""
for i in range(len(flag_enc)):
    dec += chr((ord(flag_enc[i]) - ord(key[i])) % 26 + offset)
print(dec)

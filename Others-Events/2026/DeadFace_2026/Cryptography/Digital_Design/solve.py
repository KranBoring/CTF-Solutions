from Crypto.Util.number import *
import string
alpha = string.ascii_uppercase
message = "001100000 10110011 001110101 100111010 010101000 101111101 100101100 00001100 10001010 100000010 0100001110"
keys = "XXONO NXNOA OAOON NXXAO NAAXO XANXO ANOXA ANOXN NONOX ANXAX AOAAX"

taget = {"X":2,"A":2,"N":1,"O":2}

new_message = ""
flag = ""
offset = 0
for key in keys:
    if key == ' ':
        offset += 1
        flag += alpha[int(new_message, 2)- 1]
        new_message = ""
        continue
    if taget[key] == 2:
        twobits = message[offset: offset + 2]
        bit1 = int(twobits[0])
        bit2 = int(twobits[1])
        if key == "X":
            new_message += str(bit1^bit2)
        elif key == "A":
            new_message += str(bit1&bit2)
        elif key == "O":
            new_message += str(bit1|bit2)
    elif taget[key] == 1:
        new_message += "0" if int(message[offset]) == 1 else '1'
    offset += taget[key] if key != ' ' else 1
flag += alpha[int(new_message, 2) - 1]
print(flag)
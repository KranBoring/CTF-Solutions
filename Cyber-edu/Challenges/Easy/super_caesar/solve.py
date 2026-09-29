keyup = 2
keylower = 9
cipher = "YnuNmQPGhQWqCXGUxuXnFVqrUVCUMhQdaHuCIrbDIcUqnKxbPORYTzVCDBlmAqtKnEJcpED"


flag = ""
for char in cipher:
    if char.isupper():
        flag += chr((ord(char) - ord('A') - keyup) % 26 + ord('A'))
    else :
        flag += chr((ord(char) - ord('a') - keylower) % 26 + ord('a'))
print("ECSC{" + flag[flag.index("FlAGis") + 6:] + "}")
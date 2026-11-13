from CTF_Crypto_Attack.Util.parsers import parsers
from Crypto.Util.number import long_to_bytes
data = parsers('output.txt')
flag = long_to_bytes(data['c'] // ((data['y_A']**2 * data['y_B']**2) % data['p']))
print(flag)
from CTF_Crypto_Attack.Util.parsers import parsers
from itertools import combinations
from CTF_Crypto_Attack.RSA import hastad_s_broadcast
from Crypto.Util.number import long_to_bytes

data = parsers('output.txt',multi_value=True)

cts_Ns = {cts:N for cts,N in zip(data['c'], data['n'])}

for i in combinations(cts_Ns, 3):
    res = hastad_s_broadcast(list(i),[cts_Ns[j] for j in i])
    if res is None:
        continue
    else:
        print(long_to_bytes(res).decode())
        break

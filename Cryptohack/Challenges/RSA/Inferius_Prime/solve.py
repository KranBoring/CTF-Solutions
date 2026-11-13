from Crypto.Util.number import long_to_bytes
from orjson import dumps,loads
import requests
from sage.all import *
#from CTF_Crypto_Attack.Util.factordb import get_factors
n = 984994081290620368062168960884976209711107645166770780785733
e = 65537
ct = 948553474947320504624302879933619818331484350431616834086273

url = "https://factordb.com/rpc"
json = {"method":"get_factors","params":{"target":{"expr":str(n)}}}

res = requests.post(url, json=json).json()

factors = [int(i['base']) for i in res['result']['factors']]
#res = get_factors(n)
factors = [int(i['base']) for i in res['result']['factors']]
p, q = factors
T = (q- 1)*(p - 1)
d = pow(0x10001, -1, T)
flag = long_to_bytes(pow(ct, d, n)).decode()
print(flag)




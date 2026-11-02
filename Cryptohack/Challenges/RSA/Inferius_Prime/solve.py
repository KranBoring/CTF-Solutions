from Crypto.Util.number import long_to_bytes
from orjson import dumps,loads
import requests
from sage.all import *

n = 984994081290620368062168960884976209711107645166770780785733
e = 65537
ct = 948553474947320504624302879933619818331484350431616834086273

url = "https://factordb.com/rpc"
json = {"method":"get_factors","params":{"target":{"expr":str(n)}}}

res = requests.post(url, json=json).json()

factors = [int(i['base']) for i in res['result']['factors']]

p, q = factors
T = (q- 1)*(p - 1)




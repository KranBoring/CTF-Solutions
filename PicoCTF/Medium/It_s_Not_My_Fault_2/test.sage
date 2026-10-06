from sage.all import crt
from sympy.ntheory.modular import solve_congruence

data = crt([13,17],[82,96])
print(data)
datanew = solve_congruence((13,82),(17,96))
print(datanew)
print(pow(data,-1,(82)*(96)))
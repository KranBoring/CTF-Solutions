from sage.all import *

Z = GF(29)
num = [14,6,11]
list_num2 = []
for i in range(29):
    list_num2.append(Z(pow(i,2)))
for i in num:
    if i in list_num2:
        print(list_num2.index(i) ," ",i)


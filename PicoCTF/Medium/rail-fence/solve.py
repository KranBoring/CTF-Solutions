with open("message.txt","r") as f:
    cipher = f.read()
L = len(cipher)
N = 4

flag = [None for i in range(L)] 

list_index = [i for i in range(0, L, 2*N - 2)]

count = 0
for i in range(L):
    flag[list_index[count]] = cipher[i]
    if count == len(list_index) - 1:
        newlist = []
        for index in list_index:
            if (0 <= index - 1 < L) and (flag[index - 1] is None) and ((index - 1) not in newlist):
                newlist.append(index - 1)
            if (0 <= index + 1 < L) and (flag[index + 1] is None) and ((index + 1) not in newlist):
                newlist.append(index + 1)
        list_index = [i for i in newlist if i < L]
        count = 0
    else:
        count += 1
print("".join(flag))
    
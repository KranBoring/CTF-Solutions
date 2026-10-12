from pwn import *
import json

host = "socket.cryptohack.org"
port = 13383

def readjson():
    resp = json.loads(io.readline().strip().decode())
    print(resp)
    return resp
def payjson(json_file):
    req = json.dumps(json_file)
    print(req)
    io.sendline(req.encode())

VALUES = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six',
          'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
SUITS = ['Clubs', 'Hearts', 'Diamonds', 'Spades']
    
desk = [f"{value} of {suit}" for suit in SUITS for value in VALUES]

def countwin(res):
    global win
    if "Correct!" in res["msg"]:
        win += 1

def findindex(value, suit):
    return desk.index(f"{value} of {suit}")

def checkhand(hand):
    data = hand.split(' ')
    value = data[0]
    suit = data[2]
    return value,suit

def recoverState():
    global current_hand
    state = []
    json_test = autojson()

    for r in range(11):
        respone = readjson()
        countwin(respone)
        if int(respone["round"]) < 33:
            payjson(json_test)
        value, suit = checkhand(respone["hand"])
        state.append(findindex(value, suit))
        current_hand = (value,suit)
    return sum([a * 52** i for i,a in enumerate(state[::-1])])

def next(state):
    global p,a,b
    state_data = (state * a + b) % p
    return state_data

def rebase(n, base=52):
    if n < base:
        return [n]
    else:
        return [n % base] + rebase(n//base, base)

def checksuit(suit1, suit2):
    return (SUITS.index(suit1) > SUITS.index(suit2))

def checkvalue(value1, value2):
    return (VALUES.index(value1) > VALUES.index(value2))

def autojson(state = "lower"):
    return {"choice":state}
while True:
    while True:
        win = 0
        try:
            io = remote(host, port)
            x1 = recoverState()
            x2 = recoverState()
            x3 = recoverState()
            break
        except Exception:
            io.close()
            continue
    p = 2**61 - 1
    d2 = x2 - x1
    d3 = x3 - x2
    a = d3 * pow(d2, -1, p)
    b = x2 - a * x1
    state = x3
    index_desk = []
    while True:
        try:
            if index_desk == []:
                state = next(state)
                index_desk = rebase(state)
            hidden_index = index_desk.pop()
            hidden_value,hidden_suit = checkhand(desk[hidden_index])
            if checkvalue(current_hand[0],hidden_value):
                payjson(autojson("low"))
            elif checkvalue(hidden_value,current_hand[0]):
                payjson(autojson("high"))
            elif checksuit(current_hand[1],hidden_suit):
                payjson(autojson("low"))
            elif checksuit(hidden_suit,current_hand[1]):
                payjson(autojson("high"))
            else:
                payjson(autojson())
            current_hand = (hidden_value,hidden_suit)
            res = readjson()
            countwin(res)
        except Exception:
            break
    if "crypto{" not in res["msg"]:
        continue
    else:
        break
print(res["msg"])
print(f"So tran thang:{win}\nSo tran thua:{200 - win}\nTy le thang:{win/200}\nThan bai🔥🔥🔥🔥🔥")
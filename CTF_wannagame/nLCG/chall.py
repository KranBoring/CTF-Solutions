from secrets import randbelow 
from Crypto.Util.number import getPrime
import sys
with open('/flag.txt','r') as f:
    flag = f.read().strip()

part1, part2 = flag[:len(flag)//2], flag[len(flag)//2:]
class LCG:
    def __init__(self):
        self.m = getPrime(256)
        self.a = randbelow(self.m - 1)
        self.c = randbelow(self.m - 1)  
        self.x = randbelow(self.m - 1)

    def __call__(self):
        self.x = (self.a * self.x + self.c) % self.m
        return self.x 
    
def chall1(): 
    print("First part: ")
    lcg = LCG()
    print("I will give you some hint")
    for _ in range(5):
        print(lcg())
        sys.stdout.flush()
    win = True 
    for _ in range(3): 
        chall = lcg()
        guess = int(input("Can you guess the number? ")) 
        if guess != chall: 
            win = False 
    if win:
        print(part1)
    else:
        print("Suck my dick!")
        sys.exit(0)

def chall2():
    print("Second part: ")
    nlcg = nLCG()
    print("You will need this ")
    print(f"A = {nlcg.A}")
    print(f"B = {nlcg.B}")
    print(f"C = {nlcg.C}")
    print(f"D = {nlcg.D}")
    print("Now there will be no more hints")
    for _ in range(10):
        print(nlcg.transform(nlcg()))
        sys.stdout.flush()
    win = True
    for _ in range(3):
        chall = nlcg()
        guess = int(input("Can you guess the number? "))
        if guess != chall:
            win = False
    if win:
        print(part2)
    else:
        print("Suck my dick!")
        sys.exit(0)
        
MENU = """Choose an option:
1. Solve for first part
2. Solve for second part
3. Exit
> """
while True: 
    choice = input(MENU)
    if choice == "1":
        chall1()
    elif choice == "2":
        chall2()
    elif choice == "3":
        sys.exit(0)
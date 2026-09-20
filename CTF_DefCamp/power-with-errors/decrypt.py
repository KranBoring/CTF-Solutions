from Crypto.Util.number import *
from sage.all import *
import secrets

def xor(A,B):
    return bytes([a^b for (a,b) in zip(A,B)])

p=289681150111530694174556323703782825681
n=10
t=5
c=3

def main():
    pass

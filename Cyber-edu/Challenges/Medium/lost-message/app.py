#!/usr/bin/python3
import sys, random, binascii, hashlib, re, math, os
from string import ascii_uppercase as asc
from itertools import product as d


upper = {ascii:chr(ascii) for ascii in range(65,91)}
lower = {ascii:chr(ascii) for ascii in range(97,123)}
digit = {ascii:chr(ascii) for ascii in range(48,58)}

with open("text.txt", "r") as myfile:
    data = myfile.readline()


def premessage(text):
    
    text = text.replace("_", "Q")

    return text

def enc4(text, key, debug=False):

    r = [['\n' for i in range(len(text))] 
                  for j in range(key)] 
      
    
    dir_down = False
    row, col = 0, 0
      
    for i in range(len(text)): 
          
        
        if (row == 0) or (row == key - 1): 
            dir_down = not dir_down 
          
         
        r[row][col] = text[i] 
        col += 1
          
         
        if dir_down: 
            row += 1
        else: 
            row -= 1
    
    result = [] 
    for i in range(key): 
        for j in range(len(text)): 
            if r[i][j] != '\n': 
                result.append(r[i][j]) 
    return("" . join(result))


def enc3(text, key):
    t=lambda x: x.upper().replace('J','I')
    s=[]
    for _ in t(key+asc):

        if _ not in s and _ in asc:

            s.append(_)

    m=[s[i:i+5] for i in range(0,len(s),5)]
    enc={row[i]+row[j]:row[(i+1)%5]+row[(j+1)%5] for row in m for i,j in d(range(5),repeat=2) if i!=j}
    enc.update({col[i]+col[j]:col[(i+1)%5]+col[(j+1)%5] for col in zip(*m) for i,j in d(range(5),repeat=2) if i!=j})
    enc.update({m[i1][j1]+m[i2][j2]:m[i1][j2]+m[i2][j1] for i1,j1,i2,j2 in d(range(5),repeat=4) if i1!=i2 and j1!=j2})
    l=re.findall(r'(.)(?:(?!\1)(.))?',''.join([_ for _ in t(text) if _ in asc]))

    return ''.join(enc[a+(b if b else 'Z')] for a,b in l)


def enc2(string, key): 
    for c in string:
        o = ord(c)
        if (o not in upper and o not in lower) or o in digit:
            yield o
        else:
            if o in upper and o + key % 26 in upper:
                yield o + key % 26
            elif o in lower and o + key % 26 in lower:
                yield o + key % 26.
            else: 
                yield o + key % 26 -26

    
    

def enc1(msg, key): 
    cipher = "" 
    k_indx = 0
    msg_len = float(len(msg)) 
    msg_lst = list(msg) 
    key_lst = sorted(list(key)) 
    col = len(key) 
    row = int(math.ceil(msg_len / col)) 
    fill_null = int((row * col) - msg_len) 
    msg_lst.extend('z' * fill_null)   
    matrix = [msg_lst[i: i + col]  
            for i in range(0, len(msg_lst), col)] 
    
     
    for _ in range(col): 
        curr_idx = key.index(key_lst[k_indx]) 
        cipher += ''.join([row[curr_idx]  
                        for row in matrix]) 
        k_indx += 1
    
    return cipher 

cipher = enc1(enc3(enc4(premessage(data), 13),"recomanded"), "zxdfiuypka")
cipher = "".join(map(chr, enc2(cipher, 35)))

print(cipher)

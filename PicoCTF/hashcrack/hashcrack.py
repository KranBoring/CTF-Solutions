import hashlib

#
user_hash = '482c811da5d5b4bc6d497ffa98491e38'
with open("rockyou.txt",encoding="latin-1") as rock:
    for password in rock:
        if hashlib.md5(password.encode()).hexdigest() == user_hash:
            print(password)
            print(user_hash)

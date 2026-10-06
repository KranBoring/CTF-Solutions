start = "15371"
endmd5 = "aff6ee"
import string
import hashlib

i = 0
while True:
    pay = start + f"{i:09x}"
    print(pay)
    i += 1
    value = hashlib.md5(pay.encode()).hexdigest()
    if value[-6:] == endmd5:
        print(pay)
        break
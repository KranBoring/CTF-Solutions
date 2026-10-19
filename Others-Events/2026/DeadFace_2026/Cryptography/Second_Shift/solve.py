from pwn import xor

plaintext = open("relay-heartbeat.json","rb").read()
ciphertext = open("relay-heartbeat.enc","rb").read()
ciphertext_2 = open("relay-tasking.enc","rb").read()
print(xor(xor(ciphertext,ciphertext_2),plaintext))
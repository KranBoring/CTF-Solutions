from CTF_Crypto_Attack.Symmetric import break_substitution_cipher

ciphertext = open("public/flag.txt").read()
corpus = open("public/study-guide.txt").read()

flag = break_substitution_cipher(ciphertext=ciphertext, corpus=corpus, restarts=26)

print(flag)
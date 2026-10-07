from pwn import *

io = remote("xebec.cylabacademy.net",15300)

SQUARE_SIZE = 6

def generate_square(alphabet):
	assert len(alphabet) == pow(SQUARE_SIZE, 2)
	matrix = []
	for i, letter in enumerate(alphabet):
		if i % SQUARE_SIZE == 0:
			row = []
		row.append(letter)
		if i % SQUARE_SIZE == (SQUARE_SIZE - 1):
			matrix.append(row)
	return matrix

def get_index(letter, matrix):
	for row in range(SQUARE_SIZE):
		for col in range(SQUARE_SIZE):
			if matrix[row][col] == letter:
				return (row, col)
	print("letter not found in matrix.")
	exit()

def decrypt_pair(pair, matrix):
    p1 = get_index(pair[0], matrix)
    p2 = get_index(pair[1], matrix)

    if p1[0] == p2[0]:
        return matrix[p1[0]][(p1[1] - 1)  % SQUARE_SIZE] + matrix[p2[0]][(p2[1] - 1)  % SQUARE_SIZE]
    elif p1[1] == p2[1]:
        return matrix[(p1[0] - 1)  % SQUARE_SIZE][p1[1]] + matrix[(p2[0] - 1)  % SQUARE_SIZE][p2[1]]
    else:
        return matrix[p1[0]][p2[1]] + matrix[p2[0]][p1[1]]

def decrypt_string(ciphertext, matrix):
	result = ""
	for i in range(0, len(ciphertext), 2):
		result += decrypt_pair(ciphertext[i:i+2], matrix)
	return result

def payload(payload):
	io.sendline(str(payload).encode())
	print(payload)

def reuntil(text):
	res = io.recvuntil(text.encode())
	print(res.decode())

reuntil("Here is the alphabet: ")
alphabet = io.recvline().strip().decode()
print(alphabet)
reuntil("Here is the encrypted message: ")
ciphertext = io.readline().strip().decode()
print(ciphertext)
reuntil("What is the plaintext message? ")

#Payload
matrix = generate_square(alphabet)
m = decrypt_string(ciphertext, matrix)
payload(m)

# Nhan co
reuntil("Congratulations! Here's the flag: ")
cipherflag = io.recvline().strip().decode()
print(cipherflag)
io.interactive()

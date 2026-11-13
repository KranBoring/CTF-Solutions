import os
import random
import sys

BANNER = '''
Welcome to secure vault! It is known that Vigenère cipher is secure if the key
is at as long as the message. So I am willing to share you my encrypted password
as many times as you wish. Can you recover it? I guess not!
'''.strip()

# Generates n numbers randomly, from [0, 1, ..., 25].
def generate_key(n):
    return [random.randint(0, 26) for _ in range(n)]

# Encrypt the message using Vigenère cipher
# https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
def encrypt(message, key):
    ciphertext = ''
    for m, k in zip(message, key):
        # Gets the character code (ASCII) of m.
        ## "A" corresponds to 65, "B" corresponds to 66, ..., and "Z" corresponds to 90.
        m = ord(m)
        ## Subtracts 65 to make "A" corresponds to 0, "B" corresponds to 1, etc.
        m = m - 65

        # "Encrypt" the message using the key. It is equivalent to adding the two numbers and taking modulo 26.
        # The resulting number should be 0, 1, ... or 25.
        c = (m + k) % 26

        # Convert the number to a character by first adding 65.
        c = c + 65
        # Then using the "chr" function, which converts the ASCII code to the character.
        c = chr(c)

        # Finally, append the character to the ciphertext
        ciphertext += c

    return ciphertext

def main():
    FLAG = os.environ.get('FLAG', 'hkcert22{***REDACTED***}')

    # Generate a 16 character password. One example being "IQWFMFDWMDHSXXNT".
    password = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=16))

    print(BANNER)

    while True:
        operation = input('> ')
        if operation == 'e': # E for encryption
            key = generate_key(16)
            ciphertext = encrypt(password, key)
            print(ciphertext)
        elif operation == 'g': # G for guess
            print('Okay. What is my password?')
            guess_password = input('> ')
            if password != guess_password:
                print('Wrong!')
                sys.exit(1)
            else:
                break

    print(f'How did you guess my password? Here is your flag... {FLAG}')


# For the ones who doesn't trust my code. I am writing some test cases :)
def test():
    pass

if __name__ == '__main__':
    test()
    main()

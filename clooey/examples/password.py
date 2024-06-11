import random

length = int(input("Password length: "))
letters = input("Allowed characters: ")

password = ''.join([random.choice(letters) for _ in range(length)])

print(f"Generated password: {password}")
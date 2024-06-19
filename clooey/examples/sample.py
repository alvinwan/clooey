"""Tell me about you

A simple hello world application to greet you!
"""

name = input("Enter your name: ")
age = int(input("Enter your age: "))
city = input("Enter your city [Seattle]: ") or 'Seattle'

print(f"Welcome to {city}, {name} ({age})!")
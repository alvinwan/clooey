name = input("Enter your name: ")

if name[0].lower() not in 'aeiou':
    name = name[1:] + name[:1]  # only move first letter to the end of not vowel
name += 'ay'

print(f"Your name in pig latin: {name}")
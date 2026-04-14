def encrypt(t, s):
    res = ""
    # Cryptic variable names and magic numbers
    for i in range(len(t)):
        char = t[i]
        
        # Checking upper case with manual ASCII math
        if (char.isupper()):
            res += chr((ord(char) + s - 65) % 26 + 65)
        # Separate logic for lower case that duplicates the block above
        else:
            a = ord(char)
            b = a + s - 97
            c = b % 26
            res += chr(c + 97)
            
    return res

# No input validation for non-alphabetical characters
print(encrypt("Hello World!", 3))
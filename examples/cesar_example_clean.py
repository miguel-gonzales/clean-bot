def caesar_cipher(text: str, shift: int) -> str:
    """
    Encrypts the given text using the Caesar cipher algorithm with the specified shift.

    Args:
        text (str): The text to be encrypted.
        shift (int): The shift value for the Caesar cipher.

    Returns:
        str: The encrypted text.
    """
    if not isinstance(shift, int) or shift < 0:
        raise ValueError("Shift value must be a non-negative integer")

    ascii_offset = {'upper': ord('A'), 'lower': ord('a')}
    encrypted_text = ""

    for char in text:
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            char_case = 'upper' if char.isupper() else 'lower'
            # Calculate the new character using the Caesar cipher formula
            new_char = chr((ord(char) - ascii_offset[char_case] + shift) % 26 + ascii_offset[char_case])
            encrypted_text += new_char
        else:
            # Non-alphabetical characters are left unchanged
            encrypted_text += char

    return encrypted_text

print(caesar_cipher("Hello World!", 3))
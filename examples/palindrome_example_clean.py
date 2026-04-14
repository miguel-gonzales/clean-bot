def is_palindrome(input_string: str) -> bool:
    """
    Checks if the given string is a palindrome, ignoring case.

    Args:
        input_string (str): The string to check.

    Returns:
        bool: True if the string is a palindrome, False otherwise.
    """
    # Convert the string to lowercase to ignore case
    lower_string = input_string.lower()
    
    # Use slicing to reverse the string, which is more efficient and Pythonic
    reversed_string = lower_string[::-1]
    
    # Simplify the conditional logic by directly returning the comparison result
    return lower_string == reversed_string

# Example usage
print(is_palindrome("Racecar"))  # Returns True
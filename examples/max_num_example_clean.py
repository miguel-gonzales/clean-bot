def find_max(numbers):
    """
    Finds the maximum value in a list of numbers.

    Args:
        numbers (list): A list of numbers.

    Returns:
        str: A string indicating the maximum value in the list.
    """
    # Use the built-in max() function to find the maximum value
    max_value = max(numbers)
    
    # Return a string indicating the maximum value
    return f"The biggest one is: {max_value}"

my_nums = [10, 5, 22, 14]
print(find_max(my_nums))
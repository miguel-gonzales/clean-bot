def add_numbers(num1: int, num2: int) -> int:
    """
    Adds two numbers together.

    Args:
        num1 (int): The first number to add.
        num2 (int): The second number to add.

    Returns:
        int: The sum of num1 and num2.

    Raises:
        TypeError: If either num1 or num2 is not a number.
    """
    # Check if both num1 and num2 are numbers
    if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
        raise TypeError("Both inputs must be numbers")

    # Add the two numbers together
    return num1 + num2
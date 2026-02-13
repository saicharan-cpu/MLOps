# calculator.py
def add(a, b):
    """
    Returns the sum of two numbers.

    Args:
        a (int/float): First operand.
        b (int/float): Second operand.

    Returns:
        int/float: Sum of a and b.

    Raises:
        TypeError: If either argument is not a number.
    """
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        raise TypeError("Both arguments must be numeric types.")
    return a + b


def subtract(a, b):
    """
    Returns the difference between two numbers.

    Args:
        a (int/float): Minuend.
        b (int/float): Subtrahend.

    Returns:
        int/float: Result of a - b.

    Raises:
        TypeError: If either argument is not a number.
    """
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        raise TypeError("Both arguments must be numeric types.")
    return a - b


def multiply(a, b):
    """
    Returns the product of two numbers.

    Args:
        a (int/float): First factor.
        b (int/float): Second factor.

    Returns:
        int/float: Product of a and b.

    Raises:
        TypeError: If either argument is not a number.
    """
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        raise TypeError("Both arguments must be numeric types.")
    return a * b


def divide(a, b):
    """
    Returns the quotient of two numbers.

    Args:
        a (int/float): Dividend.
        b (int/float): Divisor.

    Returns:
        float: Result of a / b.

    Raises:
        TypeError: If either argument is not a number.
        ZeroDivisionError: If divisor is zero.
    """
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        raise TypeError("Both arguments must be numeric types.")
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def power(base, exponent):
    """
    Raises a number to a given power.

    Args:
        base (int/float): The base number.
        exponent (int/float): The exponent.

    Returns:
        int/float: Result of base^exponent.

    Raises:
        TypeError: If either argument is not a number.
    """
    if not (isinstance(base, (int, float)) and isinstance(exponent, (int, float))):
        raise TypeError("Both arguments must be numeric types.")
    return base ** exponent
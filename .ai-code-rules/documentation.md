# Code Documentation

Clear and comprehensive documentation is essential for maintainable code. This rule ensures code is properly documented.

## Examples of Violations

```python
# Bad - Missing documentation
def calculate(a, b):
    return a * b + 2

# Bad - Incomplete documentation
def process_data(data):
    """Process the data"""
    return transform(data)

# Bad - Outdated documentation
def get_user(id):
    """Get user by ID
    Args:
        id: User ID
    Returns:
        User object
    """
    # Function now returns dict instead of User object
    return {"id": id, "name": "User"}

# Good - Complete documentation
def calculate_discount(price: float, quantity: int) -> float:
    """Calculate the discount for a given price and quantity.

    Args:
        price (float): The original price of the item
        quantity (int): The number of items purchased

    Returns:
        float: The calculated discount amount

    Raises:
        ValueError: If price is negative or quantity is less than 1

    Examples:
        >>> calculate_discount(100.0, 2)
        20.0
        >>> calculate_discount(50.0, 5)
        25.0
    """
    if price < 0 or quantity < 1:
        raise ValueError("Price must be positive and quantity must be at least 1")
    return price * quantity * 0.1
```

## Guidelines

1. Document all public functions and classes
2. Use docstrings following Google or NumPy style
3. Include:
   - Description of what the code does
   - Args/Parameters section
   - Returns section
   - Raises section (if applicable)
   - Examples (for complex functions)
4. Keep documentation up-to-date with code changes
5. Document complex algorithms or business logic
6. Use type hints for better documentation
7. Include inline comments for non-obvious code
8. Document configuration options
9. Include usage examples in documentation
10. Document edge cases and limitations
11. Keep comments concise and meaningful
12. Use consistent documentation style
13. Document API endpoints and their parameters
14. Include error codes and their meanings
15. Document environment variables and configuration

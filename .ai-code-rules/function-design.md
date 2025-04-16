# Function and Method Design

Well-designed functions are crucial for maintainable code. This rule ensures functions follow best practices for clarity, reusability, and maintainability.

## Examples of Violations

```python
# Bad - Too many responsibilities
def process_user_data(user_data, config, db_connection, email_service):
    # Validates data
    if not user_data.get('name'):
        raise ValueError("Name is required")

    # Processes data
    processed_data = transform_data(user_data)

    # Saves to database
    db_connection.save(processed_data)

    # Sends email
    email_service.send_welcome_email(user_data['email'])

    # Returns result
    return processed_data

# Good - Single responsibility
def validate_user_data(user_data):
    if not user_data.get('name'):
        raise ValueError("Name is required")
    return user_data

def process_user_data(user_data):
    return transform_data(user_data)

def save_user_data(user_data, db_connection):
    return db_connection.save(user_data)

def send_welcome_email(email, email_service):
    return email_service.send_welcome_email(email)
```

## Guidelines

1. Functions should have a single responsibility
2. Keep functions small and focused (ideally under 20 lines)
3. Use descriptive names that indicate what the function does
4. Limit the number of parameters (ideally 3 or fewer)
5. Avoid side effects when possible
6. Return values should be consistent in type
7. Document complex logic with comments
8. Use type hints for better code clarity
9. Consider using dataclasses or namedtuples for multiple return values
10. Functions should either do something or return something, not both

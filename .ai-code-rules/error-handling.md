# Proper Error Handling

Proper error handling is crucial for building robust applications. This rule ensures that errors are handled appropriately and provide meaningful feedback.

## Examples of Violations

```python
# Bad - Bare except
try:
    result = process_data(data)
except:
    pass

# Bad - Generic error message
try:
    result = process_data(data)
except Exception as e:
    print("An error occurred")

# Good - Specific exception handling with meaningful messages
try:
    result = process_data(data)
except ValueError as e:
    logger.error(f"Invalid data format: {e}")
    raise DataValidationError("Invalid input data format") from e
except ConnectionError as e:
    logger.error(f"Failed to connect to service: {e}")
    raise ServiceUnavailableError("Service temporarily unavailable") from e
```

## Guidelines

1. Never use bare `except:` clauses
2. Always specify the exception type you're catching
3. Include meaningful error messages
4. Log errors appropriately
5. Consider creating custom exception classes for domain-specific errors
6. Use exception chaining with `raise ... from e`
7. Handle exceptions at the appropriate level of abstraction
8. Clean up resources in `finally` blocks when necessary

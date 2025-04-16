# Security Best Practices

Security is crucial in modern applications. This rule ensures code follows security best practices to prevent common vulnerabilities.

## Examples of Violations

```python
# Bad - SQL Injection vulnerability
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# Bad - Hardcoded credentials
API_KEY = "secret123"
DATABASE_PASSWORD = "password123"

# Bad - Insecure random number generation
import random
def generate_token():
    return random.randint(1000, 9999)

# Good - Parameterized queries
def get_user(username):
    query = "SELECT * FROM users WHERE username = %s"
    return db.execute(query, (username,))

# Good - Environment variables
import os
API_KEY = os.getenv('API_KEY')
DATABASE_PASSWORD = os.getenv('DB_PASSWORD')

# Good - Secure random generation
import secrets
def generate_token():
    return secrets.token_hex(16)
```

## Guidelines

1. Never use string formatting for SQL queries
2. Use parameterized queries or ORMs
3. Store secrets in environment variables or secure secret managers
4. Use secure random number generators (secrets module)
5. Validate and sanitize all user input
6. Implement proper authentication and authorization
7. Use HTTPS for all external communications
8. Implement rate limiting for sensitive endpoints
9. Keep dependencies updated to patch security vulnerabilities
10. Use secure password hashing (bcrypt, Argon2)
11. Implement proper session management
12. Use CSRF protection for forms
13. Implement proper CORS policies
14. Log security events appropriately
15. Use security headers (HSTS, CSP, etc.)

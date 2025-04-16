# Performance Optimization

Efficient code is crucial for application performance. This rule ensures code follows performance best practices.

## Examples of Violations

```python
# Bad - N+1 query problem
def get_user_posts(users):
    posts = []
    for user in users:
        user_posts = db.query("SELECT * FROM posts WHERE user_id = %s", user.id)
        posts.extend(user_posts)
    return posts

# Bad - Unnecessary list creation
def process_data(data):
    result = []
    for item in data:
        result.append(transform(item))
    return result

# Bad - Inefficient string concatenation
def build_message(parts):
    message = ""
    for part in parts:
        message += part
    return message

# Good - Single query with JOIN
def get_user_posts(users):
    user_ids = [user.id for user in users]
    return db.query("""
        SELECT p.* FROM posts p
        JOIN users u ON p.user_id = u.id
        WHERE u.id IN %s
    """, (tuple(user_ids),))

# Good - List comprehension
def process_data(data):
    return [transform(item) for item in data]

# Good - Efficient string joining
def build_message(parts):
    return "".join(parts)
```

## Guidelines

1. Minimize database queries (avoid N+1 problem)
2. Use appropriate data structures
3. Avoid unnecessary object creation
4. Use list comprehensions instead of loops when appropriate
5. Use generators for large datasets
6. Cache expensive computations
7. Use efficient string operations
8. Profile code to identify bottlenecks
9. Use appropriate indexing in databases
10. Implement pagination for large datasets
11. Use async/await for I/O operations
12. Implement proper connection pooling
13. Use batch operations when possible
14. Implement proper caching strategies
15. Monitor and log performance metrics

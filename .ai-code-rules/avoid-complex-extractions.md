# Avoid Complex Extractions in Clauses

Complex extractions in clauses can make code harder to read and maintain. This rule identifies when a clause contains too many nested operations or complex logic that should be extracted into a separate function.

## Examples of Violations

```python
# Bad
if user.get('preferences', {}).get('notifications', {}).get('email', False) and \
   user.get('status') == 'active' and \
   len(user.get('subscriptions', [])) > 0:
    send_email(user)

# Good
if should_send_email(user):
    send_email(user)

def should_send_email(user):
    return (
        user.get('preferences', {}).get('notifications', {}).get('email', False) and
        user.get('status') == 'active' and
        len(user.get('subscriptions', [])) > 0
    )
```

## Guidelines

1. If a clause contains more than 3 conditions, consider extracting it
2. If a clause contains nested dictionary/object access, consider extracting it
3. If a clause contains complex boolean logic, consider extracting it
4. The extracted function should have a descriptive name that explains its purpose

# Code-related anti-patterns

This document outlines potential anti-patterns related to code quality and maintainability across different programming languages.

## Comments overuse

#### Problem

When you overuse comments or comment self-explanatory code, it can have the effect of making code _less readable_. Comments should explain why something is done, not what is being done.

#### Example

```python
# Returns the Unix timestamp of 5 minutes from the current time
def get_unix_five_min_from_now():
    # Get the current time
    now = datetime.now()

    # Convert it to a Unix timestamp
    unix_now = int(now.timestamp())

    # Add five minutes in seconds
    return unix_now + (60 * 5)
```

#### Refactoring

Prefer clear and self-explanatory function names, class names, and variable names when possible. In the example above, the function name explains well what the function does, so you likely won't need the comment before it. The code also explains the operations well through variable names and clear function calls.

You could refactor the code above like this:

```python
FIVE_MIN_IN_SECONDS = 60 * 5

def get_unix_five_min_from_now():
    now = datetime.now()
    unix_now = int(now.timestamp())
    return unix_now + FIVE_MIN_IN_SECONDS
```

We removed the unnecessary comments. We also added a constant `FIVE_MIN_IN_SECONDS`, which serves the additional purpose of giving a name to the "magic" number `60 * 5`, making the code clearer and more expressive.

## Complex error handling

#### Problem

When error handling logic becomes too complex or nested, it can make the code harder to read and maintain. This often happens when multiple error conditions need to be checked in sequence.

#### Example

```python
def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            try:
                decoded = base64.b64decode(content)
                try:
                    result = json.loads(decoded)
                    return result
                except json.JSONDecodeError:
                    return {'error': 'Invalid JSON format'}
            except base64.binascii.Error:
                return {'error': 'Invalid base64 encoding'}
    except FileNotFoundError:
        return {'error': 'File not found'}
```

#### Refactoring

Break down complex error handling into smaller, focused functions. Each function should handle one specific type of error:

```python
def process_file(file_path):
    try:
        content = read_file(file_path)
        decoded = decode_base64(content)
        return parse_json(decoded)
    except FileError as e:
        return {'error': str(e)}

def read_file(path):
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileError('File not found')

def decode_base64(content):
    try:
        return base64.b64decode(content)
    except base64.binascii.Error:
        raise FileError('Invalid base64 encoding')

def parse_json(content):
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise FileError('Invalid JSON format')

class FileError(Exception):
    pass
```

## Long parameter list

#### Problem

Functions with too many parameters are hard to understand and use. They make the code less maintainable and increase the chance of errors when calling the function.

#### Example

```python
def create_user(first_name, last_name, email, password, phone, address, city, state, zip_code, country, date_of_birth, gender, occupation):
    # ... implementation ...
```

#### Refactoring

Group related parameters into objects or data structures:

```python
class Address:
    def __init__(self, street, city, state, zip_code, country):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

class UserInfo:
    def __init__(self, first_name, last_name, email, password, phone, address, date_of_birth, gender, occupation):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.address = address
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.occupation = occupation

def create_user(user_info):
    # ... implementation ...
```

## Magic numbers and strings

#### Problem

Using literal numbers or strings directly in code without explanation makes the code harder to understand and maintain. These values often represent important business rules or configuration parameters.

#### Example

```python
def calculate_discount(price):
    if price > 100:
        return price * 0.1
    return 0

def process_status(status):
    if status == "P":
        return "Pending"
    elif status == "A":
        return "Approved"
    elif status == "R":
        return "Rejected"
```

#### Refactoring

Use named constants or enums to give meaning to these values:

```python
MIN_PRICE_FOR_DISCOUNT = 100
DISCOUNT_PERCENTAGE = 0.1

class Status:
    PENDING = "P"
    APPROVED = "A"
    REJECTED = "R"

def calculate_discount(price):
    if price > MIN_PRICE_FOR_DISCOUNT:
        return price * DISCOUNT_PERCENTAGE
    return 0

def process_status(status):
    status_map = {
        Status.PENDING: "Pending",
        Status.APPROVED: "Approved",
        Status.REJECTED: "Rejected"
    }
    return status_map.get(status, "Unknown")
```

## Deep nesting

#### Problem

Deeply nested code (multiple levels of if statements, loops, etc.) is hard to read and maintain. It often indicates that the code is trying to do too many things at once.

#### Example

```python
def process_data(data):
    if data is not None:
        if isinstance(data, dict):
            if 'items' in data:
                for item in data['items']:
                    if 'status' in item:
                        if item['status'] == 'active':
                            if 'value' in item:
                                return item['value']
    return None
```

#### Refactoring

Break down the logic into smaller functions and use early returns to reduce nesting:

```python
def process_data(data):
    if data is None:
        return None

    if not isinstance(data, dict):
        return None

    if 'items' not in data:
        return None

    return find_active_item_value(data['items'])

def find_active_item_value(items):
    for item in items:
        if is_active_item(item):
            return item.get('value')
    return None

def is_active_item(item):
    return item.get('status') == 'active'
```

## Duplicate code

#### Problem

Repeating the same or very similar code in multiple places makes maintenance difficult and increases the chance of bugs when changes are needed.

#### Example

```python
def calculate_total(items):
    total = 0
    for item in items:
        if item['type'] == 'book':
            total += item['price'] * 0.9  # 10% discount for books
        else:
            total += item['price']
    return total

def calculate_tax(items):
    tax = 0
    for item in items:
        if item['type'] == 'book':
            tax += (item['price'] * 0.9) * 0.1  # 10% tax on discounted price
        else:
            tax += item['price'] * 0.1  # 10% tax
    return tax
```

#### Refactoring

Extract common logic into reusable functions:

```python
def get_item_price(item):
    if item['type'] == 'book':
        return item['price'] * 0.9  # 10% discount for books
    return item['price']

def calculate_total(items):
    return sum(get_item_price(item) for item in items)

def calculate_tax(items):
    return sum(get_item_price(item) * 0.1 for item in items)  # 10% tax
```

## Inconsistent naming

#### Problem

Using inconsistent naming conventions makes code harder to read and understand. This includes mixing different naming styles (camelCase, snake_case) or using unclear abbreviations.

#### Example

```python
def getUserData():
    # ...

def process_user_info():
    # ...

def calc_usr_stats():
    # ...
```

#### Refactoring

Choose and stick to a consistent naming convention:

```python
def get_user_data():
    # ...

def process_user_info():
    # ...

def calculate_user_stats():
    # ...
```

## Overly complex expressions

#### Problem

Complex expressions with multiple operations and conditions are hard to read and understand. They often contain hidden bugs and are difficult to debug.

#### Example

```python
result = (x + y) * (a - b) / (c * d) if (x > 0 and y > 0) or (a < b and c > d) else (x * y) + (a / b) - (c + d)
```

#### Refactoring

Break down complex expressions into smaller, named parts:

```python
def calculate_result(x, y, a, b, c, d):
    if should_use_complex_formula(x, y, a, b, c, d):
        return complex_formula(x, y, a, b, c, d)
    return simple_formula(x, y, a, b, c, d)

def should_use_complex_formula(x, y, a, b, c, d):
    return (x > 0 and y > 0) or (a < b and c > d)

def complex_formula(x, y, a, b, c, d):
    numerator = (x + y) * (a - b)
    denominator = c * d
    return numerator / denominator

def simple_formula(x, y, a, b, c, d):
    return (x * y) + (a / b) - (c + d)
```

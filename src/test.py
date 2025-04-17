import json
import base64
from datetime import datetime

# This function has too many parameters and uses magic numbers
def createUser(firstName, lastName, email, password, phone, address, city, state, zipCode, country, dob, gender, occupation):
    # Magic numbers for validation
    if len(password) < 8:
        return {"error": "Password too short"}
    if len(phone) != 10:
        return {"error": "Invalid phone number"}
    
    # Complex nested logic
    user = {
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "password": password,
        "phone": phone,
        "address": {
            "street": address,
            "city": city,
            "state": state,
            "zip": zipCode,
            "country": country
        },
        "dob": dob,
        "gender": gender,
        "occupation": occupation,
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return user

# This function has deep nesting and complex error handling
def processUserData(data):
    if data is not None:
        if isinstance(data, dict):
            if "user" in data:
                user = data["user"]
                if "status" in user:
                    if user["status"] == "active":
                        if "profile" in user:
                            profile = user["profile"]
                            if "preferences" in profile:
                                return profile["preferences"]
    return None

# This function has duplicate code and magic strings
def calculateOrderTotal(items):
    total = 0
    for item in items:
        if item["type"] == "book":
            total += item["price"] * 0.9  # 10% discount for books
        else:
            total += item["price"]
    return total

def calculateOrderTax(items):
    tax = 0
    for item in items:
        if item["type"] == "book":
            tax += (item["price"] * 0.9) * 0.1  # 10% tax on discounted price
        else:
            tax += item["price"] * 0.1  # 10% tax
    return tax

# This function has overly complex expressions
def calculateComplexValue(x, y, a, b, c, d):
    return (x + y) * (a - b) / (c * d) if (x > 0 and y > 0) or (a < b and c > d) else (x * y) + (a / b) - (c + d)

# This function has inconsistent naming and comments overuse
def processFile(filePath):
    # Read the file
    try:
        with open(filePath, "r") as f:
            # Get the content
            content = f.read()
            
            # Try to decode base64
            try:
                # Decode the content
                decoded = base64.b64decode(content)
                
                # Try to parse JSON
                try:
                    # Parse the JSON
                    result = json.loads(decoded)
                    return result
                except json.JSONDecodeError:
                    return {"error": "Invalid JSON format"}
            except base64.binascii.Error:
                return {"error": "Invalid base64 encoding"}
    except FileNotFoundError:
        return {"error": "File not found"}

# This function uses magic strings for status codes
def processStatus(status):
    if status == "P":
        return "Pending"
    elif status == "A":
        return "Approved"
    elif status == "R":
        return "Rejected"
    else:
        return "Unknown"

# Example usage
if __name__ == "__main__":
    # Test createUser with too many parameters
    user = createUser(
        "John", "Doe", "john@example.com", "password123",
        "1234567890", "123 Main St", "New York", "NY",
        "10001", "USA", "1990-01-01", "M", "Engineer"
    )
    print(user)
    
    # Test processUserData with deep nesting
    data = {
        "user": {
            "status": "active",
            "profile": {
                "preferences": {"theme": "dark"}
            }
        }
    }
    result = processUserData(data)
    print(result)
    
    # Test order calculations with duplicate code
    items = [
        {"type": "book", "price": 20},
        {"type": "other", "price": 30}
    ]
    total = calculateOrderTotal(items)
    tax = calculateOrderTax(items)
    print(f"Total: {total}, Tax: {tax}")
    
    # Test complex value calculation
    value = calculateComplexValue(1, 2, 3, 4, 5, 6)
    print(f"Complex value: {value}")
    
    # Test status processing with magic strings
    status = processStatus("P")
    print(f"Status: {status}") 
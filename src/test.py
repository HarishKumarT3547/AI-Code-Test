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

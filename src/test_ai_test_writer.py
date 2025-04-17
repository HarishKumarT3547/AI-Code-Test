import unittest
from unittest.mock import patch, MagicMock
import json
import base64
from datetime import datetime
from src.test import (
    createUser,
    processUserData,
    calculateOrderTotal,
    calculateOrderTax,
    calculateComplexValue,
    processFile,
    processStatus
)

class TestAIReview(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.valid_user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "password123",
            "phone": "1234567890",
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zipCode": "10001",
            "country": "USA",
            "dob": "1990-01-01",
            "gender": "M",
            "occupation": "Engineer"
        }

    def test_create_user_valid_input(self):
        """Test createUser with valid input"""
        result = createUser(**self.valid_user_data)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["firstName"], "John")
        self.assertEqual(result["lastName"], "Doe")
        self.assertIn("createdAt", result)

    def test_create_user_invalid_password(self):
        """Test createUser with invalid password"""
        invalid_data = self.valid_user_data.copy()
        invalid_data["password"] = "short"
        result = createUser(**invalid_data)
        self.assertEqual(result, {"error": "Password too short"})

    def test_create_user_invalid_phone(self):
        """Test createUser with invalid phone number"""
        invalid_data = self.valid_user_data.copy()
        invalid_data["phone"] = "123"
        result = createUser(**invalid_data)
        self.assertEqual(result, {"error": "Invalid phone number"})

    def test_process_user_data_valid(self):
        """Test processUserData with valid data"""
        data = {
            "user": {
                "status": "active",
                "profile": {
                    "preferences": {"theme": "dark"}
                }
            }
        }
        result = processUserData(data)
        self.assertEqual(result, {"theme": "dark"})

    def test_process_user_data_invalid(self):
        """Test processUserData with invalid data"""
        self.assertIsNone(processUserData(None))
        self.assertIsNone(processUserData({}))
        self.assertIsNone(processUserData({"user": {}}))

    def test_calculate_order_total(self):
        """Test calculateOrderTotal with various items"""
        items = [
            {"type": "book", "price": 20},
            {"type": "other", "price": 30}
        ]
        result = calculateOrderTotal(items)
        self.assertEqual(result, 48.0)  # 20 * 0.9 + 30

    def test_calculate_order_tax(self):
        """Test calculateOrderTax with various items"""
        items = [
            {"type": "book", "price": 20},
            {"type": "other", "price": 30}
        ]
        result = calculateOrderTax(items)
        self.assertEqual(result, 4.8)  # (20 * 0.9 * 0.1) + (30 * 0.1)

    def test_calculate_complex_value(self):
        """Test calculateComplexValue with various inputs"""
        # Test case 1: x > 0 and y > 0
        result1 = calculateComplexValue(1, 2, 3, 4, 5, 6)
        # Test case 2: a < b and c > d
        result2 = calculateComplexValue(0, 0, 3, 4, 5, 4)
        self.assertIsInstance(result1, float)
        self.assertIsInstance(result2, float)

    @patch('builtins.open')
    def test_process_file_success(self, mock_open):
        """Test processFile with successful file processing"""
        # Mock file content
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = base64.b64encode(
            json.dumps({"test": "data"}).encode()
        ).decode()
        mock_open.return_value = mock_file

        result = processFile("test.txt")
        self.assertEqual(result, {"test": "data"})

    def test_process_status(self):
        """Test processStatus with various status codes"""
        self.assertEqual(processStatus("P"), "Pending")
        self.assertEqual(processStatus("A"), "Approved")
        self.assertEqual(processStatus("R"), "Rejected")
        self.assertEqual(processStatus("X"), "Unknown")

if __name__ == '__main__':
    unittest.main() 
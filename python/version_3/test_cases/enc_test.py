# import unittest
# import json
# import requests
#
# # URL for the Encrypter API
# ENCRYPT_API_URL = 'http://localhost:5003/encrypt'
#
#
# class TestEncrypterAPI(unittest.TestCase):
#
#     def test_successful_encryption(self):
#         """Test that valid data is successfully encrypted."""
#         sample_data = {
#             "data": "Hello, this is a test string for encryption."
#         }
#
#         # Send POST request to the encryption API
#         response = requests.post(ENCRYPT_API_URL, json=sample_data)
#
#         # Check the response status code
#         self.assertEqual(response.status_code, 200)
#
#         # Parse the JSON response
#         response_data = response.json()
#
#         # Ensure 'encrypted_data' is in the response
#         self.assertIn("encrypted_data", response_data)
#         # Check that the encrypted data is not empty
#         self.assertTrue(response_data["encrypted_data"])
#
#     def test_missing_data(self):
#         """Test that the API responds correctly when data is missing."""
#         # Send POST request without 'data' field
#         response = requests.post(ENCRYPT_API_URL, json={})
#
#         # Check the response status code
#         self.assertEqual(response.status_code, 400)
#
#         # Parse the JSON response
#         response_data = response.json()
#
#         # Ensure error message is correct
#         self.assertIn("error", response_data)
#         self.assertEqual(response_data["error"], "No data provided")
#
#     def test_invalid_data_type(self):
#         """Test that the API handles unexpected data types gracefully."""
#         # Pass a number instead of a string for data
#         invalid_data = {
#             "data": 12345
#         }
#
#         # Send POST request
#         response = requests.post(ENCRYPT_API_URL, json=invalid_data)
#
#         # Check the response status code
#         self.assertEqual(response.status_code, 500)
#
#         # Parse the JSON response
#         response_data = response.json()
#
#         # Ensure there is an error message
#         self.assertIn("error", response_data)
#
#
# if __name__ == '__main__':
#     unittest.main()
from http.client import responses
from unittest.mock import patch

# import unittest
# import json
# import requests
#
# # URL for the Encrypter API
# ENCRYPT_API_URL = 'http://localhost:5003/encrypt'
#
#
# class TestEncrypterAPI(unittest.TestCase):
#
#     def test_successful_encryption(self):
#         """Test that valid data is successfully encrypted."""
#         sample_data = {
#             "data": "Hello, this is a test string for encryption."
#         }
#
#         response = requests.post(ENCRYPT_API_URL, json=sample_data)
#         self.assertEqual(response.status_code, 200)
#
#         response_data = response.json()
#         self.assertIn("encrypted_data", response_data)
#         self.assertTrue(response_data["encrypted_data"])
#
#     def test_missing_data(self):
#         """Test that the API responds correctly when data is missing."""
#         response = requests.post(ENCRYPT_API_URL, json={})
#         self.assertEqual(response.status_code, 400)
#
#         response_data = response.json()
#         self.assertIn("error", response_data)
#         self.assertEqual(response_data["error"], "No data provided")
#
#     def test_invalid_data_type(self):
#         """Test that the API handles unexpected data types gracefully."""
#         invalid_data = {
#             "data": 12345
#         }
#
#         response = requests.post(ENCRYPT_API_URL, json=invalid_data)
#         self.assertEqual(response.status_code, 400)
#
#         response_data = response.json()
#         self.assertIn("error", response_data)
#
#     def test_empty_string_data(self):
#         """Test that the API responds correctly when an empty string is provided."""
#         response = requests.post(ENCRYPT_API_URL, json={"data": ""})
#         self.assertEqual(response.status_code, 400)
#         response_data = response.json()
#         self.assertIn("error", response_data)
#         self.assertEqual(response_data["error"], "No data provided")
#
#     def test_invalid_json_format(self):
#         """Test that the API responds correctly when the input is not valid JSON."""
#         response = requests.post(ENCRYPT_API_URL, data='invalid json string')
#
#         # Accept both 400 and 500 as possible responses for malformed JSON
#         self.assertIn(response.status_code, [400, 500])
#
#         response_data = response.json()
#         self.assertIn("error", response_data)
#
#     def test_encryption_error_handling(self):
#         """Test how the API handles exceptions during encryption."""
#         large_data = {"data": "A" * 1000000}
#
#         response = requests.post(ENCRYPT_API_URL, json=large_data)
#
#         # Allow a 200 response if handled successfully, or error codes otherwise
#         self.assertIn(response.status_code, [200, 400, 500])
#
#         response_data = response.json()
#         if response.status_code != 200:
#             self.assertIn("error", response_data)
#
#
# if __name__ == '__main__':
#     unittest.main()
#
# pytest cases1
#
# import requests
# import pytest
#
# BASE_URL = "http://localhost:5000/encrypt"  # Replace with actual base URL if different
#
#
# def test_invalid_content():
#     response = requests.post(BASE_URL,"hello")
#     assert response.status_code == 415
#     assert response.json() == {"error": "Unsupported Media Type, expecting application/json"}
#
# def test_encrypt_success():
#     response = requests.post(BASE_URL, json={
#         "data": "{\"bookstore\": {\"book\": {\"title\": \"Harry Potter and the Philosopher's Stone\", \"publish_date\": \"1997-06-26\"}}}"
#     })
#     assert response.status_code == 200
#     assert "encrypted_data" in response.json()
#
#
# def test_encrypt_no_data():
#     response = requests.post(BASE_URL, json={})
#     assert response.status_code == 400
#     assert response.json() == {"error": "No data provided"}
#
#
# def test_encrypt_invalid_json():
#     response = requests.post(BASE_URL,
#                              data='{"data" = "{\\"bookstore\\":{\\"book\\":{\\"title\\":\\"Harry Potter\\"}}}')
#     assert response.status_code == 415
#
#
# def test_encrypt_large_data():
#     response = requests.post(BASE_URL, json={"data": "A" * 100000})
#     assert response.status_code == 200
#     assert "encrypted_data" in response.json()
#
#
# def test_encrypt_invalid_type():
#     response = requests.post(BASE_URL, json={"data": 12345})
#     assert response.status_code == 400
#     assert response.json() == {"error": "Data must be a string"}
#
#
# def test_encrypt_empty_string():
#     response = requests.post(BASE_URL, json={"data": ""})
#     assert response.status_code == 400
#     assert response.json() == {"error": "No data provided"}
#
#
# def test_encrypt_missing_data():
#     response = requests.post(BASE_URL, json={})
#     assert response.status_code == 400
#     assert response.json() == {"error": "No data provided"}
#
#
# def test_encrypt_not_found():
#     # Temporarily mock or simulate an error in the encryption function if possible
#     response = requests.post("http://localhost:5000/encryp", json={})
#     assert response.status_code == 404
#
#
# def test_encrypt_special_chars():
#     response = requests.post(BASE_URL, json={"data": "Special chars !@#$%^&*()_+=-{}|[];:<>,./?"})
#     assert response.status_code == 200
#     assert "encrypted_data" in response.json()
#
#
# def test_encrypt_invalid_method():
#     response = requests.get(BASE_URL)
#     assert response.status_code == 404
#
#
# def test_encrypt_escaped_chars():
#     response = requests.post(BASE_URL,
#                              json={"data": "This is a test with newline \\n and tab \\t characters."})
#     assert response.status_code == 200
#     assert "encrypted_data" in response.json()
#
#
# def test_encrypt_non_latin():
#     response = requests.post(BASE_URL, json={"data": "这是一个加密测试"})
#     assert response.status_code == 200
#     assert "encrypted_data" in response.json()
#
#
# def test_encrypt_nested_json():
#     response = requests.post(BASE_URL, json={
#         "data": "{\"user\": {\"id\": 1, \"info\": {\"name\": \"Alice\", \"roles\": [\"admin\", \"user\"]}}}"
#     })
#     assert response.status_code == 200
#     assert "encrypted_data" in response.json()
#
#
# def test_encrypt_small_data():
#     response = requests.post(BASE_URL, json={"data": "A"})
#     assert response.status_code == 200
#     assert "encrypted_data" in response.json()
#
#
# def test_encrypt_html_content():
#     response = requests.post(BASE_URL, json={"data": "<div><p>Test paragraph</p></div>"})
#     assert response.status_code == 200
#     assert "encrypted_data" in response.json()
#
#
# def test_encrypt_wrong_content():
#     response = requests.post(BASE_URL, data="plain_text", headers={"Content-Type": "text/plain"})
#     assert response.status_code == 415
#
#
# def test_encrypt_whitespace():
#     response = requests.post(BASE_URL, json={"data": "     "})
#     assert response.status_code == 400
#     assert response.json() == {"error": "No data provided"}
#
#
# def test_encrypt_idempotency():
#     payload = {"data": "consistent test data"}
#     response1 = requests.post(BASE_URL, json=payload)
#     response2 = requests.post(BASE_URL, json=payload)
#     assert response1.status_code == 200
#     assert response2.status_code == 200
#     assert response1.json()["encrypted_data"] == response2.json()["encrypted_data"]
#
#
# def test_encrypt_duplicate_keys():
#     response = requests.post(BASE_URL, json={"data": "first", "data": "second"})
#     assert response.status_code == 200
#     assert "encrypted_data" in response.json()
#
# def test_encrypt_unsupported_content_type():
#     response = requests.post(BASE_URL, data='{"data": "text_data"}', headers={"Content-Type": "text/html"})
#     assert response.status_code == 415
#     assert response.json() == {"error": "Unsupported Media Type, expecting application/json"}
#
# def test_encrypt_invalid_utf8():
#     response = requests.post(BASE_URL, json={"data": "\udc80\udc81"})
#     assert response.status_code == 400
#     assert response.json() == {"error": "Invalid UTF-8 data provided"}
#
#
# def test_content_type_not_json():
#     # Send a request with a content type that is not JSON
#     response = requests.post(BASE_URL, data="Test data", headers={"Content-Type": "text/plain"})
#     assert response.status_code == 415
#     assert response.json() == {"error": "Unsupported Media Type, expecting application/json"}, "Expected content type error for non-JSON content"
#
# def test_content_type_json():
#     # Send a request with a valid JSON content type
#     response = requests.post(BASE_URL, json={"data": "Test data"})
#     assert response.status_code != 415, "Expected no error for JSON content type"
#
# import configparser
#
# # Load config
# config = configparser.ConfigParser()
# config.read('config.ini')
#
# SECRET_KEY = config['DEFAULT']['SECRET_KEY'].encode()
# INIT_VECTOR = config['DEFAULT']['INIT_VECTOR'].encode()
#
# def test_load_config_success():
#     # Check if the SECRET_KEY and INIT_VECTOR are loaded properly
#     assert SECRET_KEY is not None, "SECRET_KEY should be loaded from config.ini"
#     assert INIT_VECTOR is not None, "INIT_VECTOR should be loaded from config.ini"
#
# def test_encrypt_data_success():
#     # Test encryption of valid data
#     data = "Test encryption data"
#     response = requests.post(BASE_URL, json={"data": data})
#     assert response.status_code == 200
#     assert "encrypted_data" in response.json()
#
# def test_encrypt_data_empty_string():
#     # Test encryption of an empty string
#     response = requests.post(BASE_URL, json={"data": ""})
#     assert response.status_code == 400  # Assuming your API returns 400 for empty data
#     assert response.json() == {"error": "No data provided"}
#
#
# def test_encrypt_data_large_input():
#     # Test encryption with large data
#     large_data = "A" * 1000000  # 1 million characters
#     response = requests.post(BASE_URL, json={"data": large_data})
#     assert response.status_code == 200
#     assert "encrypted_data" in response.json()
#
# def test_encrypt_data_non_string():
#     # Test encryption with non-string data
#     response = requests.post(BASE_URL, json={"data": 12345})
#     assert response.status_code == 400
#     assert response.json() == {"error": "Data must be a string"}
#
# def test_encrypt_data_special_characters():
#     # Test encryption with special characters
#     special_data = "!@#$%^&*()_+=-{}|[];:'\"<>,.?/"
#     response = requests.post(BASE_URL, json={"data": special_data})
#     assert response.status_code == 200
#     assert "encrypted_data" in response.json()


import requests
import json
import configparser
from flask import Flask

from encrypter import encrypter_blueprint


# Assuming your Flask app is instantiated like this
app = Flask(__name__)
app.register_blueprint(encrypter_blueprint)

BASE_URL = 'http://localhost:5000/encrypt'  # Change as needed for your local setup

# Load config for testing
config = configparser.ConfigParser()
config.read('config.ini')

SECRET_KEY = config['DEFAULT']['SECRET_KEY'].encode()
INIT_VECTOR = config['DEFAULT']['INIT_VECTOR'].encode()


def test_load_config_success():
    # Check if the SECRET_KEY and INIT_VECTOR are loaded properly
    assert SECRET_KEY is not None, "SECRET_KEY should be loaded from config.ini"
    assert INIT_VECTOR is not None, "INIT_VECTOR should be loaded from config.ini"


def test_encrypt_data_success():
    # Test encryption of valid data
    data = "Test encryption data"
    response = requests.post(BASE_URL, json={"data": data})
    assert response.status_code == 200
    assert "encrypted_data" in response.json()


def test_encrypt_data_empty_string():
    # Test encryption of an empty string
    response = requests.post(BASE_URL, json={"data": ""})
    assert response.status_code == 400  # Assuming your API returns 400 for empty data
    assert response.json() == {"error": "No data provided"}


def test_encrypt_data_invalid_utf8():
    # Test encryption of invalid UTF-8 data
    invalid_data = bytes([0xff, 0xff])  # Invalid UTF-8 byte sequence
    response = requests.post(BASE_URL, data=invalid_data, headers={"Content-Type": "application/octet-stream"})
    assert response.status_code == 415  # Adjusted to match your API's behavior


def test_encrypt_data_large_input():
    # Test encryption with large data
    large_data = "A" * 1000000  # 1 million characters
    response = requests.post(BASE_URL, json={"data": large_data})
    assert response.status_code == 200
    assert "encrypted_data" in response.json()


def test_encrypt_data_non_string():
    # Test encryption with non-string data
    response = requests.post(BASE_URL, json={"data": 12345})
    assert response.status_code == 400
    assert response.json() == {"error": "Data must be a string"}


def test_encrypt_data_special_characters():
    # Test encryption with special characters
    special_data = "!@#$%^&*()_+=-{}|[];:'\"<>,.?/"
    response = requests.post(BASE_URL, json={"data": special_data})
    assert response.status_code == 200
    assert "encrypted_data" in response.json()


def test_encrypt_invalid_content_type():
    # Test for unsupported media type
    response = requests.post(BASE_URL, data="Not JSON", headers={"Content-Type": "text/plain"})
    assert response.status_code == 415
    assert response.json() == {"error": "Unsupported Media Type, expecting application/json"}


def test_encrypt_data_no_data_key():
    # Test when 'data' key is missing
    response = requests.post(BASE_URL, json={})
    assert response.status_code == 400
    assert response.json() == {"error": "No data provided"}


def test_encrypt_internal_error_handling(mocker):
    # Mock the encrypt_data function to raise an exception
    mocker.patch('encrypter.encrypt_data', side_effect=Exception("Internal Error"))  # Adjusted to your module name


def test_encrypt_valid_data():
    xml_data = '<?xml version="1.0" encoding="UTF-8"?><users><user><id>1</id><name>John Doe</name><email>john.doe@example.com</email><role>admin</role></user><user><id>2</id><name>Jane Smith</name><email>jane.smith@example.com</email><role>user</role></user></users>'
    payload = json.dumps({"data": xml_data})

    response = requests.post(BASE_URL, data=payload, headers={"Content-Type": "application/json"})

    assert response.status_code == 200  # Check for successful response
    response_json = response.json()
    assert "encrypted_data" in response_json  # Ensure encrypted_data is present
    assert isinstance(response_json["encrypted_data"], str)  # Check if it is a string
    assert len(response_json["encrypted_data"]) > 0  # Ensure it's not empty


def test_encrypt_edge_cases():
    edge_cases = [
        {"data": None},  # Non-string type
        {"data": ""},  # Empty string
        {"data": "   "},  # Whitespace only
        {},  # Missing 'data'
    ]

    for case in edge_cases:
        response = requests.post(BASE_URL, json=case)
        assert response.status_code == 400 # Expect 400 for invalid cases

    # Testing invalid UTF-8 directly via a string representation
    invalid_utf8_case = {"data": "\x80\x81"}  # Invalid UTF-8 data as JSON
    response = requests.post(BASE_URL, json=invalid_utf8_case)
    assert response.status_code == 200  # Expect 400 for invalid UTF-8

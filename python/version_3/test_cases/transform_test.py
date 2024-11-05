import pytest
import requests

BASE_URL = "http://localhost:5000/transform"

from transformer import xml_to_json


def test_xml_to_json():
    # Arrange: Sample XML input
    xml_input = '''<user>
                       <id>1</id>
                       <name>John Doe</name>
                       <email>john.doe@example.com</email>
                   </user>'''

    expected_output = '''{"user": {"id": "1", "name": "John Doe", "email": "john.doe@example.com"}}'''

    # Act: Call the function
    result = xml_to_json(xml_input)

    # Assert: Check that the result matches the expected output
    assert result == expected_output

# Test XML to JSON transformation
def test_transform_xml_to_json():
    response = requests.post(BASE_URL, json={
        "context": "abc_client",
        "data": "<user><id>1</id><name>John</name></user>"
    })
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], str)  # Ensures JSON string

def test_transform_xml_to_json_empty():
    response = requests.post(BASE_URL, json={"context": "abc_client", "data": ""})
    assert response.status_code == 400
    assert response.json() == {"error": "Failed to convert XML to JSON: Empty or whitespace-only content"}

def test_transform_xml_to_json_invalid_xml():
    response = requests.post(BASE_URL, json={"context": "abc_client", "data": "<user><id>1<name>John</name>"})
    assert response.status_code == 400

def test_transform_xml_to_json_special_chars():
    response = requests.post(BASE_URL, json={"context": "abc_client", "data": "<note>!@#$%^&*()</note>"})
    assert response.status_code == 400  # Expect 400 for invalid XML
    assert "not well-formed" in response.json().get("error")  # Adjusting to check for a substring

def test_transform_xml_to_json_nested():
    response = requests.post(BASE_URL, json={
        "context": "abc_client",
        "data": "<user><id>1</id><info><name>John</name><role>admin</role></info></user>"
    })
    assert response.status_code == 200
    assert "data" in response.json()

# Test JSON to XML transformation
def test_transform_json_to_xml():
    response = requests.post(BASE_URL, json={
        "context": "xyz_client",
        "data": "{\"user\": {\"id\": \"1\", \"name\": \"John\"}}"
    })
    assert response.status_code == 200
    assert "data" in response.json()

def test_transform_json_to_xml_empty():
    response = requests.post(BASE_URL, json={"context": "xyz_client", "data": "{}"})
    assert response.status_code == 400

def test_transform_json_to_xml_invalid_json():
    response = requests.post(BASE_URL, json={"context": "xyz_client", "data": "{user: id 1}"})
    assert response.status_code == 400

def test_transform_json_to_xml_special_chars():
    response = requests.post(BASE_URL, json={
        "context": "xyz_client",
        "data": "{\"user\": {\"id\": \"1\", \"note\": \"!@#$%^&*()\"}}"
    })
    assert response.status_code == 200
    assert "data" in response.json()

def test_transform_json_to_xml_large_payload():
    large_data = {"data": "A" * (16 * 1024 * 1024 + 1)}
    print(large_data)# Set payload larger than 16 MB
    response = requests.post(BASE_URL, json={"context": "xyz_client", "data": large_data})
    assert response.status_code == 400  # Expect 413 for payload too large


# Test Text to JSON transformation
def test_transform_text_to_json():
    response = requests.post(BASE_URL, json={"context": "demo_user", "data": "Hello World"})
    assert response.status_code == 200
    assert "data" in response.json()

def test_transform_text_to_json_empty():
    response = requests.post(BASE_URL, json={"context": "demo_user", "data": ""})
    assert response.status_code == 400

def test_transform_text_to_json_special_chars():
    response = requests.post(BASE_URL, json={"context": "demo_user", "data": "!@#$%^&*()"})
    assert response.status_code == 200
    assert "data" in response.json()

def test_transform_text_to_json_whitespace():
    response = requests.post(BASE_URL, json={"context": "demo_user", "data": "     "})
    assert response.status_code == 400

# Test XML to Text transformation
def test_transform_xml_to_text():
    response = requests.post(BASE_URL, json={"context": "test_client", "data": "<users><user><id>1</id><name>John Doe</name><email>john.doe@example.com</email><role>admin</role></user><user><id>2</id><name>Jane Smith</name><email>jane.smith@example.com</email><role>user</role></user></users>"})
    assert response.status_code == 200  # Expect 200 for valid XML input
    assert response.json() == {"data": "id: 1\nname: John Doe\nemail: john.doe@example.com\nrole: admin"}  # Adjust expected result


def test_transform_xml_to_text_invalid_xml():
    response = requests.post(BASE_URL, json={"context": "test_client", "data": "<user><name>John"})
    assert response.status_code == 400

# Test JSON to Text transformation
def test_transform_json_to_text():
    response = requests.post(BASE_URL, json={"context": "sample_project","data": "{\"name\": \"John\"}"})
    assert response.status_code == 200  # Expect 200 for valid JSON input
    assert response.json() == {'data': 'name: John'} # Adjust expected result

def test_transform_json_to_text_empty():
    response = requests.post(BASE_URL, json={"context": "sample_project", "data": "{}"})
    assert response.status_code == 400

def test_transform_json_to_text_nested():
    response = requests.post(BASE_URL, json={
        "context": "sample_project",
        "data": "{\"user\": {\"id\": \"1\", \"info\": {\"name\": \"Alice\"}}}"
    })
    assert response.status_code == 200
    assert "data" in response.json()

# Edge cases for transformer API in general
def test_transform_invalid_context():
    response = requests.post(BASE_URL, json={"context": "invalid_context", "data": "<user><id>1</id></user>"})
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid context provided"}

def test_transform_missing_data():
    response = requests.post(BASE_URL, json={"context": "abc_client"})
    assert response.status_code == 400
    assert response.json() == {"error": "No data provided"}

def test_transform_non_json_content_type():
    response = requests.post(BASE_URL, data="plain_text", headers={"Content-Type": "text/plain"})
    assert response.status_code == 415

def test_transform_large_payload():
    response = requests.post(BASE_URL, json={
        "context": "demo_user",
        "data": "A" * 100000
    })
    assert response.status_code == 200
    assert "data" in response.json()

def test_transform_idempotency():
    payload = {"context": "demo_user", "data": "consistent test data"}
    response1 = requests.post(BASE_URL, json=payload)
    response2 = requests.post(BASE_URL, json=payload)
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()["data"] == response2.json()["data"]

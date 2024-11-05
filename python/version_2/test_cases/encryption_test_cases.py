import requests
import pytest

BASE_URL = "http://localhost:5003/encrypt"  # Replace with actual base URL if different


def test_encrypt_success():
    response = requests.post(BASE_URL, json={
        "data": "{\"bookstore\": {\"book\": {\"title\": \"Harry Potter and the Philosopher's Stone\", \"publish_date\": \"1997-06-26\"}}}"
    })
    assert response.status_code == 200
    assert "encrypted_data" in response.json()


def test_encrypt_no_data():
    response = requests.post(BASE_URL, json={})
    assert response.status_code == 400
    assert response.json() == {"error": "No data provided"}


def test_encrypt_invalid_json():
    response = requests.post(BASE_URL,
                             data='{"data" = "{\\"bookstore\\":{\\"book\\":{\\"title\\":\\"Harry Potter\\"}}}')
    assert response.status_code == 415


def test_encrypt_large_data():
    response = requests.post(BASE_URL, json={"data": "A" * 100000})
    assert response.status_code == 200
    assert "encrypted_data" in response.json()


def test_encrypt_invalid_type():
    response = requests.post(BASE_URL, json={"data": 12345})
    assert response.status_code == 400
    assert response.json() == {"error": "Data must be a string"}


def test_encrypt_empty_string():
    response = requests.post(BASE_URL, json={"data": ""})
    assert response.status_code == 400
    assert response.json() == {"error": "No data provided"}


def test_encrypt_missing_data():
    response = requests.post(BASE_URL, json={})
    assert response.status_code == 400
    assert response.json() == {"error": "No data provided"}


def test_encrypt_not_found():
    # Temporarily mock or simulate an error in the encryption function if possible
    response = requests.post("http://localhost:5003/encry", json={})
    assert response.status_code == 404


def test_encrypt_special_chars():
    response = requests.post(BASE_URL, json={"data": "Special chars !@#$%^&*()_+=-{}|[];:<>,./?"})
    assert response.status_code == 200
    assert "encrypted_data" in response.json()


def test_encrypt_invalid_method():
    response = requests.get(BASE_URL)
    assert response.status_code == 405


def test_encrypt_escaped_chars():
    response = requests.post(BASE_URL,
                             json={"data": "This is a test with newline \\n and tab \\t characters."})
    assert response.status_code == 200
    assert "encrypted_data" in response.json()


def test_encrypt_non_latin():
    response = requests.post(BASE_URL, json={"data": "这是一个加密测试"})
    assert response.status_code == 200
    assert "encrypted_data" in response.json()


def test_encrypt_nested_json():
    response = requests.post(BASE_URL, json={
        "data": "{\"user\": {\"id\": 1, \"info\": {\"name\": \"Alice\", \"roles\": [\"admin\", \"user\"]}}}"
    })
    assert response.status_code == 200
    assert "encrypted_data" in response.json()


def test_encrypt_small_data():
    response = requests.post(BASE_URL, json={"data": "A"})
    assert response.status_code == 200
    assert "encrypted_data" in response.json()


def test_encrypt_html_content():
    response = requests.post(BASE_URL, json={"data": "<div><p>Test paragraph</p></div>"})
    assert response.status_code == 200
    assert "encrypted_data" in response.json()


def test_encrypt_wrong_content():
    response = requests.post(BASE_URL, data="plain_text", headers={"Content-Type": "text/plain"})
    assert response.status_code == 415


def test_encrypt_whitespace():
    response = requests.post(BASE_URL, json={"data": "     "})
    assert response.status_code == 400
    assert response.json() == {"error": "No data provided"}


def test_encrypt_idempotency():
    payload = {"data": "consistent test data"}
    response1 = requests.post(BASE_URL, json=payload)
    response2 = requests.post(BASE_URL, json=payload)
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()["encrypted_data"] == response2.json()["encrypted_data"]


def test_encrypt_duplicate_keys():
    response = requests.post(BASE_URL, json={"data": "first", "data": "second"})
    assert response.status_code == 200
    assert "encrypted_data" in response.json()

import pytest
from flask import Flask
from processor import processor_blueprint  # Update with your actual module name

# Create a Flask application instance for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(processor_blueprint)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# Test for successful processing
def test_process_data_success(client):
    response = client.post('/', json={
        "data": "EjdIKPzgMHPr4xXb/xhJYJgARxgvJNL04bzHfjEHsGbw4/REUXU4WzRox9SCBF8/nMiZTJmiaHwaBj5SljEfe4YRlQJaX2KNpBia9JcrkGTlaHiemNWxMQw6iwKzoNvepkviMeZpOD2EyopMcH59mKkIk5kL3JuyUWZw9yp5+uhtHf3xWM2916pl9EVcHsYGbemIzECQ2s8y25Qq4LHv6vFO0u80Vj66vX9ZL7VD3dYhxPZ7VacodN09FmMoICsqz1mk9+MOJGJ2qofGyLNuHOiDFSDCfagExHHCfY4DnvMYyUUojzbVjt8/ZVEleOVjJKp+3aGmPejSM1ni5o89yj7i8nkSu54+BKY=",
        "context": "abc_client"
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert "decrypted_data" in json_data
    assert "transformed_data" in json_data
    assert "encrypted_data" in json_data

# Test for missing data
def test_process_data_missing_data(client):
    response = client.post('/', json={"context": "abc_client"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing data or context key"}

# Test for missing context
def test_process_data_missing_context(client):
    response = client.post('/', json={"data": "encrypted_data"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing data or context key"}

# Test for decrypt API failure
def test_process_data_decrypt_failure(client):
    response = client.post('/', json={
        "data": "encrypted_data_with_invalid_context",
        "context": "abc_client"
    })

    # Here you can set your DECRYPTER_API_URL to respond with a failure in your test environment
    assert response.status_code == 500
    assert response.get_json() == {"error": "Failed to decrypt data"}

# Test for transform API failure
def test_process_data_transform_failure(client):
    response = client.post('/', json={
        "data": "JgARxgvJNL04bzHfjEHsGbw4/REUXU4WzRox9SCBF8/nMiZTJmiaHwaBj5SljEfe4YRlQJaX2KNpBia9JcrkGTlaHiemNWxMQw6iwKzoNvepkviMeZpOD2EyopMcH59mKkIk5kL3JuyUWZw9yp5+uhtHf3xWM2916pl9EVcHsYGbemIzECQ2s8y25Qq4LHv6vFO0u80Vj66vX9ZL7VD3dYhxPZ7VacodN09FmMoICsqz1mk9+MOJGJ2qofGyLNuHOiDFSDCfagExHHCfY4DnvMYyUUojzbVjt8/ZVEleOVjJKp+3aGmPejSM1ni5o89yj7i8nkSu54+BKY=",
        "context": "abc_client"
    })

    # Here you can set your TRANSFORMER_API_URL to respond with a failure in your test environment
    assert response.status_code == 500
    assert response.get_json() =={"error": "Failed to decrypt data"}

# Test for encrypt API failure
def test_process_data_encrypt_failure(client):
    response = client.post('/', json={
        "data": "zHfjEHsGbw4/REUXU4WzRox9SCBF8/nMiZTJmiaHwaBj5SljEfe4YRlQJaX2KNpBia9JcrkGTlaHiemNWxMQw6iwKzoNvepkviMeZpOD2EyopMcH59mKkIk5kL3JuyUWZw9yp5+uhtHf3xWM2916pl9EVcHsYGbemIzECQ2s8y25Qq4LHv6vFO0u80Vj66vX9ZL7VD3dYhxPZ7VacodN09FmMoICsqz1mk9+MOJGJ2qofGyLNuHOiDFSDCfagExHHCfY4DnvMYyUUojzbVjt8/ZVEleOVjJKp+3aGmPejSM1ni5o89yj7i8nkSu54+BKY=",
        "context": "abc_client"
    })

    # Here you can set your ENCRYPT_API_URL to respond with a failure in your test environment
    assert response.status_code == 500
    assert response.get_json() == {"error": "Failed to decrypt data"}

# Test for general exception
def test_process_data_exception(client):
    response = client.post('/', json={
        "data": "b/xhJYJgARxgvJNL04bzHfjEHsGbw4/REUXU4WzRox9SCBF8/nMiZTJmiaHwaBj5SljEfe4YRlQJaX2KNpBia9JcrkGTlaHiemNWxMQw6iwKzoNvepkviMeZpOD2EyopMcH59mKkIk5kL3JuyUWZw9yp5+uhtHf3xWM2916pl9EVcHsYGbemIzECQ2s8y25Qq4LHv6vFO0u80Vj66vX9ZL7VD3dYhxPZ7VacodN09FmMoICsqz1mk9+MOJGJ2qofGyLNuHOiDFSDCfagExHHCfY4DnvMYyUUojzbVjt8/ZVEleOVjJKp+3aGmPejSM1ni5o89yj7i8nkSu54+BKY=",
        "context": "abc_client"
    })

    # Simulate a general error
    assert response.status_code == 500
    assert response.get_json() == {"error": "Failed to decrypt data"}


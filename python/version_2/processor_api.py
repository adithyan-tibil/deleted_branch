import json

from flask import Flask, request, jsonify
import requests
import configparser

# Initialize ConfigParser
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

DECRYPTOR_API_URL = config['urls']['DECRYPTOR_API_URL']
TRANSFORMER_API_URL = config['urls']['TRANSFORMER_API_URL']
ENCRYPT_API_URL = config['urls']['ENCRYPT_API_URL']
@app.route('/process', methods=['POST'])
def process_data():
    try:
        # Get input data and context from the request
        input_data = request.json.get('data')
        context_key = request.json.get('context')

        if not input_data or not context_key:
            return jsonify({"error": "Missing data or context key"}), 400

        # Call Decryptor API
        decrypt_payload = {
            "data": input_data
        }
        decrypt_response = requests.post(DECRYPTOR_API_URL, json=decrypt_payload)

        if decrypt_response.status_code != 200:
            return jsonify({"error": "Failed to decrypt data", "details": decrypt_response.text}), 500

        decrypted_data = decrypt_response.json()['data']
        print("Decrypted Data:", decrypted_data)

        # Call Transformer API with context
        transform_payload = {
            "context": context_key,
            "data": decrypted_data
        }
        transform_response = requests.post(TRANSFORMER_API_URL, json=json.dumps(transform_payload))

        if transform_response.status_code != 200:
            return jsonify({"error": "Failed to transform data", "details": transform_response.text}), 500

        transformed_data = transform_response.json()['data']
        print("Transformed Data:", transformed_data)

        # Call Encryptor API
        encrypt_payload = {
            "data": transformed_data
        }
        encrypt_response = requests.post(ENCRYPT_API_URL, json=encrypt_payload)

        if encrypt_response.status_code != 200:
            return jsonify({"error": "Failed to encrypt transformed data", "details": encrypt_response.text}), 500

        encrypted_data = encrypt_response.json()['encrypted_data']
        print("Encrypted Data:", encrypted_data)

        # Return the response
        return jsonify({
            "decrypted_data": decrypted_data,
            "transformed_data": transformed_data,
            "encrypted_data": encrypted_data
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5005, debug=True)

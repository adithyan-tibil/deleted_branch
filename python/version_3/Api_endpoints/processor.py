import json

from flask import Blueprint, request, jsonify
import requests
import configparser

processor_blueprint = Blueprint('processor', __name__)

config = configparser.ConfigParser()
config.read('config.ini')


DECRYPTER_API_URL = config['API']['DECRYPTER_URL']
TRANSFORMER_API_URL = config['API']['TRANSFORMER_URL']
ENCRYPT_API_URL = config['API']['ENCRYPT_URL']

@processor_blueprint.route('/', methods=['POST'])
def process_data():
    try:
        input_data = request.json.get('data')
        context_key = request.json.get('context')

        if not input_data or not context_key:
            return jsonify({"error": "Missing data or context key"}), 400

        decrypt_payload = {
            "data": input_data
        }
        decrypt_response = requests.post(DECRYPTER_API_URL, json=decrypt_payload)

        if decrypt_response.status_code != 200:
            return jsonify({"error": "Failed to decrypt data"}), 500

        decrypted_data = decrypt_response.json()['data']
        print("Decrypted Data:", decrypted_data)

        transform_payload = {
            "context": context_key,
            "data": decrypted_data
        }
        transform_response = requests.post(TRANSFORMER_API_URL, json=transform_payload)

        if transform_response.status_code != 200:
            return jsonify({"error": "Failed to transform data"}), 500

        transformed_data = transform_response.json()['data']
        print("Transformed Data:", transformed_data)

        encrypt_payload = {
            "data": transformed_data
        }
        encrypt_response = requests.post(ENCRYPT_API_URL, json=encrypt_payload)

        if encrypt_response.status_code != 200:
            return jsonify({"error": "Failed to encrypt transformed data"}), 500

        encrypted_data = encrypt_response.json()['encrypted_data']
        print("Encrypted Data:", encrypted_data)

        return jsonify({
            "decrypted_data": decrypted_data,
            "transformed_data": transformed_data,
            "encrypted_data": encrypted_data
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

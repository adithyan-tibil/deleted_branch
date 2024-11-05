
from flask import Flask, request, jsonify
import base64
from Crypto.Cipher import AES
import configparser


app = Flask(__name__)

# Initialize ConfigParser
config = configparser.ConfigParser()
config.read('config.ini')

SECRET_KEY = config['secrets']['SECRET_KEY'].encode('utf-8')
INIT_VECTOR = config['secrets']['INIT_VECTOR'].encode('utf-8')

def encrypt_data(data):
    cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=INIT_VECTOR)
    ciphertext, auth_tag = cipher.encrypt_and_digest(data.encode())
    encrypted_data = ciphertext + auth_tag
    return base64.b64encode(encrypted_data).decode()

@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Check content type first
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type, expecting application/json"}), 415

    try:
        # Parse input as JSON
        input_data = request.get_json(force=True)
        if 'data' not in input_data:
            return jsonify({"error": "No data provided"}), 400

        data = input_data['data']

        # Check for data type and content
        if not isinstance(data, str):
            return jsonify({"error": "Data must be a string"}), 400

        # Validate that data is not empty or whitespace
        if data.strip() == "":
            return jsonify({"error": "No data provided"}), 400

        # Validate UTF-8 encoding
        try:
            data.encode('utf-8')  # This will raise an exception if data is not valid UTF-8
        except UnicodeEncodeError:
            return jsonify({"error": "Invalid UTF-8 data provided"}), 400

        # Encrypt the input data
        encrypted_data = encrypt_data(data)
        return jsonify({"encrypted_data": encrypted_data}), 200

    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

if __name__ == '__main__':
    app.run(port=5003, debug=True)



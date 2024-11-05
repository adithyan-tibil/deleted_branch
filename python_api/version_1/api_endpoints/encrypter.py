from flask import Blueprint, request, jsonify
import base64
from Crypto.Cipher import AES
import configparser

bp = Blueprint('encrypter', __name__)

# Load config
config = configparser.ConfigParser()
config.read('config.ini')

SECRET_KEY = config['DEFAULT']['SECRET_KEY'].encode()
INIT_VECTOR = config['DEFAULT']['INIT_VECTOR'].encode()

def encrypt_data(data):
    cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=INIT_VECTOR)
    ciphertext, auth_tag = cipher.encrypt_and_digest(data.encode())
    encrypted_data = ciphertext + auth_tag
    return base64.b64encode(encrypted_data).decode()

@bp.route('/', methods=['POST'])
def encrypt():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type, expecting application/json"}), 415

    try:
        input_data = request.get_json(force=True)
        if 'data' not in input_data:
            return jsonify({"error": "No data provided"}), 400

        data = input_data['data']

        if not isinstance(data, str):
            return jsonify({"error": "Data must be a string"}), 400

        if data.strip() == "":
            return jsonify({"error": "No data provided"}), 400

        try:
            data.encode('utf-8')  # This will raise an exception if data is not valid UTF-8
        except UnicodeEncodeError:
            return jsonify({"error": "Invalid UTF-8 data provided"}), 400

        encrypted_data = encrypt_data(data)
        return jsonify({"encrypted_data": encrypted_data}), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

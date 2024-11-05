from flask import Blueprint, request, jsonify
import base64
from Crypto.Cipher import AES
import configparser

bp = Blueprint('decrypter', __name__)

config = configparser.ConfigParser()
config.read('config.ini')

SECRET_KEY = config['DEFAULT']['SECRET_KEY'].encode()
INIT_VECTOR = config['DEFAULT']['INIT_VECTOR'].encode()

def decrypt_file(encrypted_data_b64):
    encrypted_data = base64.b64decode(encrypted_data_b64)
    auth_tag = encrypted_data[-16:]
    ciphertext = encrypted_data[:-16]
    cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=INIT_VECTOR)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, auth_tag)
    return decrypted_data.decode('utf-8')

@bp.route('/', methods=['POST'])
def decrypt_data():
    try:
        data = request.json.get('data')

        if not data:
            return jsonify({"error": "No data provided"}), 400
        decrypted_data = decrypt_file(data)

        return jsonify({"data": decrypted_data}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

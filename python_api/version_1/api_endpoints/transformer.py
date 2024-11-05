
from flask import Blueprint, request, jsonify
import xmltodict
import json
import configparser

bp = Blueprint('transformer', __name__)

# Load config
config = configparser.ConfigParser()
config.read('config.ini')
context_transformers = {key: value for key, value in config['CONTEXT'].items()}

# Conversion functions
def xml_to_json(content):
    try:
        if not content.strip():
            raise ValueError("Empty or whitespace-only content")
        data_dict = xmltodict.parse(content)
        return json.dumps(data_dict)
    except Exception as e:
        return jsonify({"error": f"Failed to convert XML to JSON: {str(e)}"}), 400

def json_to_xml(content):
    try:
        if not content.strip():
            raise ValueError("Empty or whitespace-only content")
        data_dict = json.loads(content)
        return xmltodict.unparse(data_dict, pretty=True)
    except Exception as e:
        return jsonify({"error": f"Failed to convert JSON to XML: {str(e)}"}), 400

def text_to_json(content):
    if not content.strip():
        return jsonify({"error": "Input text is empty or whitespace"}), 400
    return json.dumps({"text": content})

def xml_to_text(content):
    try:
        if not content.strip():
            raise ValueError("Empty or whitespace-only content")
        data_dict = xmltodict.parse(content)
        text_data = '\n'.join(f"{key}: {value}" for key, value in data_dict['users']['user'][0].items())
        return text_data
    except Exception as e:
        return jsonify({"error": f"Failed to convert XML to Text: {str(e)}"}), 400

def json_to_text(content):
    try:
        print(content)
        if content == "{}":
            return jsonify({"error": "Empty JSON content provided"}), 400
        data_dict = json.loads(content)
        print(data_dict)
        text_data = '\n'.join(f"{key}: {value}" for key, value in data_dict.items())
        print(text_data)
        return text_data
    except Exception as e:
        return jsonify({"error": f"Failed to convert JSON to Text: {str(e)}"}), 400

# Define the transform route
@bp.route('/', methods=['POST'])
def transform():
    # Check for the content type
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type. Expected application/json"}), 415

    try:
        request_data = request.get_json(force=True)  # force=True will raise an error if the data is not JSON
        context_key = request_data.get('context')
        content = request_data.get('data')

        # Validate inputs
        if not context_key or content is None:
            return jsonify({"error": "No data provided"}), 400

        # Get the transformer function based on context
        transformer_key = context_transformers.get(context_key)
        if not transformer_key:
            return jsonify({"error": "Invalid context provided"}), 400

        transformer_function = globals().get(transformer_key)
        if not transformer_function:
            return jsonify({"error": f"Transformer function '{transformer_key}' not implemented"}), 500

        # Perform transformation
        transformed_data = transformer_function(content)
        if isinstance(transformed_data, tuple):
            return transformed_data  # For error tuples (json, status)

        return jsonify({"data": transformed_data}), 200

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

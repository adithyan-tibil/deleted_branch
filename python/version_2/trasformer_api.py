from flask import Flask, request, jsonify
import xmltodict
import json
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

context_transformers = {key: value for key, value in config['clients'].items()}

def xml_to_json(content):
    try:
        data_dict = xmltodict.parse(content)
        json_data = json.dumps(data_dict)
        return json_data
    except Exception as e:
        raise

def json_to_xml(content):
    try:
        data_dict = json.loads(content)
        xml_data = xmltodict.unparse(data_dict, pretty=True)
        return xml_data
    except Exception as e:
        raise
def text_to_json(content):
    try:
        json_data = json.dumps({"text": content})
        print("Text to JSON:", json_data)
        return json_data
    except Exception as e:
        print("Error in text_to_json:", str(e))
        raise

def xml_to_text(content):
    try:
        data_dict = xmltodict.parse(content)
        # Convert the data dictionary to a simple text representation
        text_data = '\n'.join(f"{key}: {value}" for key, value in data_dict['users']['user'][0].items())
        print("XML to Text:", text_data)
        return text_data
    except Exception as e:
        print("Error in xml_to_text:", str(e))
        raise

def json_to_text(content):
    try:
        data_dict = json.loads(content)  # Ensure input is valid JSON
        # Create a readable string format
        text_data = '\n'.join(f"{key}: {value}" for key, value in data_dict['user'].items())
        print("JSON to Text:", text_data)
        return text_data
    except Exception as e:
        print("Error in json_to_text:", str(e))
        raise

@app.route('/transform', methods=['POST'])
def transform():
    try:
        context_key = request.json.get('context')
        content = request.json.get('data')

        if not context_key or not content:
            return jsonify({"error": "Missing context or data"}), 400

        # Get the transformer based on context
        transformer_key = context_transformers.get(context_key)
        if not transformer_key:
            return jsonify({"error": f"No transformer found for the given context '{context_key}'"}), 400

        # Get the function dynamically
        transformer_function = globals().get(transformer_key)
        if not transformer_function:
            return jsonify({"error": f"Transformer function '{transformer_key}' not implemented"}), 500

        # Transform the data
        transformed_data = transformer_function(content)
        return jsonify({"data": transformed_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)

from flask import Flask
from version_3.Api_endpoints.encrypter import encrypter_blueprint
from version_3.Api_endpoints.decrypter import decrypter_blueprint
from version_3.Api_endpoints.transformer import transformer_blueprint
from version_3.Api_endpoints.processor import processor_blueprint

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


app.register_blueprint(encrypter_blueprint, url_prefix='/encrypt')
app.register_blueprint(decrypter_blueprint, url_prefix='/decrypt')
app.register_blueprint(transformer_blueprint, url_prefix='/transform')
app.register_blueprint(processor_blueprint, url_prefix='/process')

if __name__ == '__main__':
    app.run(port=5000, debug=True)

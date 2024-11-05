from flask import Flask
from api_endpoints import encrypter, decrypter, processor, transformer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.register_blueprint(encrypter.bp, url_prefix='/encrypt/')
app.register_blueprint(decrypter.bp, url_prefix='/decrypt/')
app.register_blueprint(transformer.bp, url_prefix='/transform/')
app.register_blueprint(processor.bp, url_prefix='/process/')


@app.route('/ping', methods=["GET"])
def ping_api():
    return "OK"


if __name__ == '__main__':
    app.run(port=5000, debug=True)

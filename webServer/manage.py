from flask import Flask
from flask.json import jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', "POST"])
def test_hello():
    return jsonify({'msg':'hello flask'})

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5001)
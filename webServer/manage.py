from flask import Flask
from flask.json import jsonify
from flask.templating import render_template

app = Flask(__name__)


@app.route('/', methods=['GET', "POST"])
def test_hello():
    return jsonify({'msg': 'hello flask'})


@app.route('/show_page', methods=['GET', 'POST'])
def show_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

from flask.json import jsonify
from flask.templating import render_template
from flask import Blueprint

weibo = Blueprint('weibo', __name__, template_folder='templates')


@weibo.route('/test', methods=['GET', "POST"])
def test_hello():
    return jsonify({'msg': 'hello flask'})


@weibo.route('/', methods=['GET', 'POST'])
def show_page():
    return render_template('list.html')

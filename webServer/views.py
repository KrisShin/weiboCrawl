from flask.json import jsonify
from flask.templating import render_template
from flask import Blueprint
from models import Topic, Feed, Comment
from db_init import db

weibo = Blueprint('weibo', __name__, template_folder='templates')


@weibo.route('/test', methods=['GET', "POST"])
def test_hello():
    return jsonify({'msg': 'hello flask'})


@weibo.route('/', methods=['GET', 'POST'])
def show_page():
    return render_template('list.html')

@weibo.route('/add_test_topic', methods=['GET', 'POST'])
def test_add_topic():
    '''
    from views import test_add_topic
    test_add_topic()
    '''
    t = Topic()
    t.name = 'test_topic'
    t.hot = 10
    db.session.add(t)
    db.session.commit()
    print('Done')
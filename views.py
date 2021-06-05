from flask.json import jsonify
from flask.templating import render_template
from flask import Blueprint, request
from werkzeug.utils import redirect
from models import Topic, Feed, Comment
from db_init import db

import jieba

weibo = Blueprint('weibo', __name__, template_folder='templates')


@weibo.route('/test', methods=['GET', "POST"])
def test_hello():
    '''
    测试返回 hello flask
    '''
    return jsonify({'msg': 'hello flask'})


@weibo.route('/', methods=['GET', 'POST'])
def show_page():
    '''
    测试返回页面
    '''
    topic_list = Topic.query.order_by(Topic.hot).all()
    topic_list = [dict(topic) for topic in topic_list]
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 5))

    feed_list = Feed.query
    total = feed_list.count(
    )//page_size if feed_list.count() % page_size == 0 else feed_list.count()//page_size+1
    feed_list = feed_list.offset(page*page_size).limit(page_size)
    feed_list = [dict(feed) for feed in feed_list]
    return render_template('index.html', topic_list=topic_list, feed_list=feed_list, total=total, page=page)


@weibo.route('/all_topic', methods=['GET'])
def api_get_all_topic():
    topic_list = Topic.query.order_by(Topic.hot).all()
    topic_list = [dict(topic) for topic in topic_list]
    return jsonify(topic_list)


@weibo.route('/all_comment', methods=['GET'])
def api_get_all_comment():
    comment_list = Comment.query.all()
    comment_list = [dict(comment) for comment in comment_list]
    return jsonify(comment_list)


@weibo.route('/test_data', methods=['GET'])
def add_test_data():
    '''
    add some data for test
    '''
    from random import randint
    from datetime import datetime

    for t_id in range(3):
        t = Topic(name=f'test{t_id}')
        db.session.add(t)
        db.session.commit()
        for f_id in range(3):
            f = Feed(mid=str(randint(1000, 9999)), topic=t,
                     content=f'feed {f_id} of topic {t.name}')
            f.forward_count = randint(99, 999)
            f.comment_count = randint(99, 999)
            f.like_count = randint(99, 999)
            f.publish_time = datetime.now()
            db.session.add(f)
            db.session.commit()
            for c_id in range(3):
                c = Comment(id=str(randint(1000, 9999)), feed=f,
                            content=f'comment {c_id} of feed {f.mid}')
                c.publish_time = datetime.now()
                c.like_count = randint(99, 999)
                c.reply_count = randint(99, 999)
                c.reply_like = randint(99, 999)
                db.session.add(c)
                db.session.commit()

    return jsonify({'msg': 'ok'})


@weibo.route('/search', methods=['GET'])
def search_feed():
    '''
    TODO: use Jieba to split words, and search it by sql statement with "like".
    '''
    key_string = request.args.get('search_str')
    print(key_string)
    if not key_string.split():
        return redirect('/')

    keywords = jieba.cut(key_string, cut_all=True)

    pre_sql_string = '''select id from topic where '''
    word_split_string = []
    for word in keywords:
        word_split_string.append(f'''name like '%{word}%' ''')
    key_sql_string = ' or '.join(word_split_string)
    sql_string = pre_sql_string + key_sql_string + ';'

    res = db.session.execute(sql_string)

    topic_id_list = [t[0] for t in res]

    feed_list = [dict(feed) for feed in Feed.query.filter(
        Feed.topic_id.in_(topic_id_list)).all()]

    topic_list = Topic.query.order_by(Topic.hot).all()
    topic_list = [dict(topic) for topic in topic_list]
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 5))
    feed_count = len(feed_list)
    total = feed_count//page_size if feed_count//page_size == 0 else feed_count//page_size+1

    return render_template('index.html', topic_list=topic_list, feed_list=feed_list[(page-1)*page_size:page*page_size], page=page, total=total)


@weibo.route('/api/update_crawl_data', methods=['GET'])
def update_crawl_data():
    from spiders import weibo_hot
    from threading import Thread

    job = Thread(target=weibo_hot.main, args=(50,))

    job.start()
    return jsonify({'msg': 'OK'})


@weibo.route('/feed', methods=['GET'])
def feed_page():
    mid = request.args.get('mid')
    topic_list = Topic.query.order_by(Topic.hot).all()
    topic_list = [dict(topic) for topic in topic_list]

    feed = Feed.query.filter_by(mid=mid).first()
    comment_list = [dict(comment) for comment in feed.comments]
    return render_template('post.html', feed=dict(feed), comment_list=comment_list, topic_list=topic_list)

from flask.json import jsonify
from flask.templating import render_template
from flask import Blueprint
from models import Topic, Feed, Comment
from db_init import db

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
    return render_template('index.html')


@weibo.route('/all_topic', methods=['GET'])
def api_get_all_topic():
    topic_list = Topic.query.order_by(Topic.hot).all()
    topic_list = [dict(topic) for topic in topic_list]
    return jsonify(topic_list)


@weibo.route('/all_feed', methods=['GET'])
def api_get_all_feed():
    feed_list = Feed.query.all()
    feed_list = [dict(feed) for feed in feed_list]
    return jsonify(feed_list)


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


def migrate_mongo_to_mysql():
    '''
    TODO:
    {
        "_id" : ObjectId("60b909f0c2a19ae3fae062ee"),
        "mid" : "4643945000996897",
        "link" : "https://weibo.com/1792951112/Kird24bkZ",
        "publishTime" : "2021-06-03 10:10",
        "from" : "微博视频号",
        "topicList" : [ 
            "#自信绽放 笑着见#"
        ],
        "contentList" : [ 
            "\n                                                                                                                        用自然美学与动人科技结合的", 
            " 守护你的自信笑容，从今天开始", 
            "。", 
            " ​​​​                                            "
        ],
        "shareCount" : "100万+",
        "commentCount" : "100万+",
        "likeCount" : "4613862",
        "user" : {
            "headPic" : "https://tvax2.sinaimg.cn/crop.261.201.600.600.1024/6ade4348ly8ge5avdm8jbj20u00u075k.jpg?KID=imgbed,tva&Expires=1622750234&ssig=Wwg6CwayR9",
            "nickname" : "X玖少年团肖战DAYTOY",
            "homepage" : "https://weibo.com/xiaozhan1"
        }
    }
    '''
    pass


def search_feed():
    '''
    TODO: use Jieba to split words, and search it by sql statement with "like".
    '''
    pass

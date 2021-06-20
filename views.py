import random
from flask.json import jsonify
from flask.templating import render_template
from flask import Blueprint, request
from werkzeug.utils import redirect
from models import Topic, Feed, Comment
from db_init import db


import jieba

# 创建蓝图用于管理url
weibo = Blueprint('weibo', __name__, template_folder='templates')


@weibo.route('/test', methods=['GET', "POST"])
def test_hello():
    '''
    测试接口 返回 hello flask
    '''
    return jsonify({'msg': 'hello flask'})


@weibo.route('/', methods=['GET', 'POST'])
def show_page():
    '''
    返回首页数据
    '''
    # 获取热度最高的前8个Topic 左下角展示的那一列
    topic_list = Topic.query.order_by(Topic.hot.desc()).limit(8).all()
    # 格式化Topic对象为dict对象用于返回json格式
    topic_list = [dict(topic) for topic in topic_list]

    # 获取传入的分页参数, 如果没有那么默认当前页面是第一页, 每页展示5条微博
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 5))

    feed_list = Feed.query
    # total是计算分页总页数的, 如果条数除每页条数正好除尽, 那么总页数就是商, 否则总页数是商+1
    total = feed_list.count(
    )//page_size if feed_list.count() % page_size == 0 else feed_list.count()//page_size+1
    # 取page页的page_size条数据
    feed_list = feed_list.order_by(Feed.publish_time.desc()).offset(page*page_size).limit(page_size)
    # 全部格式化为dict对象才能返回
    feed_list = [dict(feed) for feed in feed_list]
    return render_template('index.html', topic_list=topic_list, feed_list=feed_list, total=total, page=page)


@weibo.route('/all_topic', methods=['GET'])
def api_get_all_topic():
    '''
    测试接口 用于获取所有的topic
    '''
    topic_list = Topic.query.order_by(Topic.hot).all()
    topic_list = [dict(topic) for topic in topic_list]
    return jsonify(topic_list)


@weibo.route('/all_comment', methods=['GET'])
def api_get_all_comment():
    '''
    测试接口 用于获取所有的comment
    '''

    comment_list = Comment.query.all()
    comment_list = [dict(comment) for comment in comment_list]
    return jsonify(comment_list)


@weibo.route('/test_data', methods=['GET'])
def add_test_data():
    '''
    测试接口 用于新增一些随机数据到数据库
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
def feed_page_filter_by_keyword():
    '''
    搜索接口 用于搜索相关字段
    使用jieba对输入的字符串进行分词, 并按照分词后的结果模糊搜索相关的topic, 并返回关联的feed
    '''
    # 获取参数
    key_string = request.args.get('search_str')
    # 如果使用的是屏蔽关键词, 那么exclued是True
    exclude = bool(request.args.get('exclude'))
    if not key_string.split():
        # 如果输入空字符串, 或者不输入内容直接点击搜索, 那么重定向到首页
        return redirect('/')

    # jieba分词关键字
    keywords = jieba.cut(key_string, cut_all=True)

    # sql语句, 因为分词结果较为复杂, 为了效率使用sql语句一次查询
    pre_sql_string = '''select id from topic where '''
    # 用于存放分出的关键词来返回
    words = []
    # 拼接sql语句
    word_split_string = []
    for word in keywords:
        if exclude:
            word_split_string.append(f'''name not like '%{word}%' ''')
        else:
            words.append(word)
            word_split_string.append(f'''name like '%{word}%' ''')
    if exclude:
        key_sql_string = ' and '.join(word_split_string)
    else:
        key_sql_string = ' or '.join(word_split_string)
    sql_string = pre_sql_string + key_sql_string + ';'

    res = db.session.execute(sql_string)

    # 获取跟搜索关键词相关的topic的ID
    topic_id_list = [t[0] for t in res]

    # feed的id列表, 用于去重
    feed_id_list = []
    feed_list = []

    # 获取过滤出的topic下的所有feed
    for topic in Topic.query.filter(Topic.id.in_(topic_id_list)).all():
        for feed in topic.feeds:
            if feed.mid not in feed_id_list:
                feed_id_list.append(feed.mid)
                feed_list.append(feed)

    # 将所有获得的帖子按照发布时间排序, 新发布的帖子排到前面
    feed_list = sorted(feed_list, key=lambda feed:feed.publish_time, reverse=True)

    # 热度前8的topic
    topic_list = Topic.query.order_by(Topic.hot.desc()).limit(8).all()
    topic_list = [dict(topic) for topic in topic_list]
    # 分页相关
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 1000))
    feed_count = len(feed_list)
    total = feed_count//page_size if feed_count//page_size == 0 else feed_count//page_size+1

    return render_template('index.html',
                           topic_list=topic_list,
                           feed_list=feed_list[(
                               page-1)*page_size:page*page_size],
                           page=page,
                           words=words,
                           total=total)


@weibo.route('/api/update_crawl_data', methods=['GET'])
def update_crawl_data():
    '''
    开启一个线程启动爬虫程序
    '''
    from spiders import weibo_hot
    from threading import Thread

    # 爬取条数 随机80-100，不建议太多，数量太多或者爬虫太频繁可能触发微博反爬机制
    crawl_number = random.randint(80, 100) 

    # 单独开启一个线程运行爬虫程序, 避免请求挂起
    job = Thread(target=weibo_hot.run_spider, args=(crawl_number,))

    job.start()
    return jsonify({'msg': 'OK'})


@weibo.route('/feed', methods=['GET'])
def feed_page():
    '''
    微博正文详情页面
    '''
    # 获取参数
    mid = request.args.get('mid')
    # 热门话题
    topic_list = Topic.query.order_by(Topic.hot.desc()).limit(8).all()
    topic_list = [dict(topic) for topic in topic_list]

    feed = Feed.query.filter_by(mid=mid).first()
    # 获取feed的所有comment并格式化为dict
    comment_list = [dict(comment) for comment in feed.comments]
    return render_template('post.html', feed=dict(feed), comment_list=comment_list, topic_list=topic_list)


@weibo.route('/topic', methods=['GET'])
def feed_page_filter_by_topic():
    '''
    按话题过滤feed
    '''
    # 热门话题
    topic_list = Topic.query.order_by(Topic.hot.desc()).limit(8).all()
    topic_list = [dict(topic) for topic in topic_list]

    # 获取参数
    topic_id = request.args.get('topic')
    topic_obj = Topic.query.filter_by(id=int(topic_id)).first()

    # 该topic下的feed
    feed_list = [dict(feed) for feed in topic_obj.feeds]
    
    # 分页
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 1000))
    feed_count = len(feed_list)
    total = feed_count//page_size if feed_count//page_size == 0 else feed_count//page_size+1

    return render_template('index.html',
                           topic_list=topic_list,
                           feed_list=feed_list[(
                               page-1)*page_size:page*page_size],
                           page=page,
                           total=total)

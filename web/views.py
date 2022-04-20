import random

from flask.json import jsonify
from flask.templating import render_template
from flask import Blueprint, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import jieba
from werkzeug.utils import redirect

from web.global_variable import db, login_manager, default_resp
from web.models import Topic, Weibo, Comment, User

# 创建蓝图用于管理url
weibo_bp = Blueprint('weibo', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def home_page_content():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 5))

    weibo_list = Weibo.query
    # total是计算分页总页数的, 如果条数除每页条数正好除尽, 那么总页数就是商, 否则总页数是商+1
    total = (
        weibo_list.count() // page_size
        if weibo_list.count() % page_size == 0
        else weibo_list.count() // page_size + 1
    )
    # 取page页的page_size条数据
    weibo_list = (
        weibo_list.order_by(Weibo.publish_time.desc())
        .offset(page * page_size)
        .limit(page_size)
    )
    # 全部格式化为dict对象才能返回
    weibo_list = [dict(weibo) for weibo in weibo_list]
    resp = default_resp
    resp.update(
        {
            'weibo_list': weibo_list,
            'total': total,
            'page': page,
        }
    )
    return resp


@weibo_bp.route('/home', methods=['GET', 'POST'])
@login_required
def show_page():
    '''
    返回首页数据
    '''
    # 获取热度最高的前8个Topic 左下角展示的那一列
    topic_list = Topic.query.order_by(Topic.hot.desc()).limit(8).all()
    # 格式化Topic对象为dict对象用于返回json格式
    topic_list = [dict(topic) for topic in topic_list]

    resp = home_page_content()
    resp.update(
        {
            'topic_list': topic_list,
        }
    )
    return render_template('index.html', **resp)


@weibo_bp.route('/all_topic', methods=['GET'])
def api_get_all_topic():
    '''
    测试接口 用于获取所有的topic
    '''
    topic_list = Topic.query.order_by(Topic.hot).all()
    topic_list = [dict(topic) for topic in topic_list]
    return jsonify(topic_list)


@weibo_bp.route('/all_comment', methods=['GET'])
def api_get_all_comment():
    '''
    测试接口 用于获取所有的comment
    '''

    comment_list = Comment.query.all()
    comment_list = [dict(comment) for comment in comment_list]
    return jsonify(comment_list)


@weibo_bp.route('/test_data', methods=['GET'])
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
            f = Weibo(
                mid=str(randint(1000, 9999)),
                topic=t,
                content=f'weibo {f_id} of topic {t.name}',
            )
            f.forward_count = randint(99, 999)
            f.comment_count = randint(99, 999)
            f.like_count = randint(99, 999)
            f.publish_time = datetime.now()
            db.session.add(f)
            db.session.commit()
            for c_id in range(3):
                c = Comment(
                    id=str(randint(1000, 9999)),
                    weibo=f,
                    content=f'comment {c_id} of weibo {f.mid}',
                )
                c.publish_time = datetime.now()
                c.like_count = randint(99, 999)
                c.reply_count = randint(99, 999)
                c.reply_like = randint(99, 999)
                db.session.add(c)
                db.session.commit()

    return jsonify({'msg': 'ok'})


@weibo_bp.route('/search', methods=['GET'])
@login_required
def weibo_page_filter_by_keyword():
    '''
    搜索接口 用于搜索相关字段
    使用jieba对输入的字符串进行分词, 并按照分词后的结果模糊搜索相关的topic, 并返回关联的weibo
    '''
    # 获取参数
    key_string = request.args.get('search_str')
    # 如果使用的是屏蔽关键词, 那么exclued是True
    exclude = bool(request.args.get('exclude'))
    if not key_string.split():
        # 如果输入空字符串, 或者不输入内容直接点击搜索, 那么重定向到首页
        return redirect('/home')

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

    # weibo的id列表, 用于去重
    weibo_id_list = []
    weibo_list = []

    # 获取过滤出的topic下的所有weibo
    for topic in Topic.query.filter(Topic.id.in_(topic_id_list)).all():
        for weibo in topic.weibos:
            if weibo.mid not in weibo_id_list:
                weibo_id_list.append(weibo.mid)
                weibo_list.append(weibo)

    # 将所有获得的帖子按照发布时间排序, 新发布的帖子排到前面
    weibo_list = sorted(weibo_list, key=lambda weibo: weibo.publish_time, reverse=True)

    # 热度前8的topic
    topic_list = Topic.query.order_by(Topic.hot.desc()).limit(8).all()
    topic_list = [dict(topic) for topic in topic_list]
    # 分页相关
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 1000))
    weibo_count = len(weibo_list)
    total = (
        weibo_count // page_size
        if weibo_count // page_size == 0
        else weibo_count // page_size + 1
    )

    resp = default_resp
    resp.update(
        {
            'topic_list': topic_list,
            'weibo_list': weibo_list[(page - 1) * page_size : page * page_size],
            'page': page,
            'total': total,
            'words': words,
        }
    )
    return render_template('index.html', **resp)


@weibo_bp.route('/api/update_crawl_data', methods=['GET'])
@login_required
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


@weibo_bp.route('/weibo', methods=['GET'])
@login_required
def weibo_page():
    '''
    微博正文详情页面
    '''
    # 获取参数
    mid = request.args.get('mid')
    # 热门话题
    topic_list = Topic.query.order_by(Topic.hot.desc()).limit(8).all()
    topic_list = [dict(topic) for topic in topic_list]

    weibo = Weibo.query.filter_by(mid=mid).first()
    # 获取weibo的所有comment并格式化为dict
    comment_list = [dict(comment) for comment in weibo.comments]

    resp = default_resp
    resp.update(
        {
            'weibo': dict(weibo),
            'comment_list': comment_list,
            'topic_list': topic_list,
        }
    )
    return render_template('post.html', **resp)


@weibo_bp.route('/topic', methods=['GET'])
@login_required
def weibo_page_filter_by_topic():
    '''
    按话题过滤weibo
    '''
    # 热门话题
    topic_list = Topic.query.order_by(Topic.hot.desc()).limit(8).all()
    topic_list = [dict(topic) for topic in topic_list]

    # 获取参数
    topic_id = request.args.get('topic')
    topic_obj = Topic.query.filter_by(id=int(topic_id)).first()

    # 该topic下的weibo
    weibo_list = [dict(weibo) for weibo in topic_obj.weibos]

    # 分页
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 1000))
    weibo_count = len(weibo_list)
    total = (
        weibo_count // page_size
        if weibo_count // page_size == 0
        else weibo_count // page_size + 1
    )

    resp = default_resp
    resp.update(
        {
            'topic_list': topic_list,
            'weibo_list': weibo_list[(page - 1) * page_size : page * page_size],
            'page': page,
            'total': total,
        }
    )

    return render_template('index.html', **resp)


@weibo_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        resp = default_resp
        return render_template('login.html', **resp)
    elif request.method == 'POST':
        form = request.form
        username = form.get('username')
        password = form.get('password')
        if not all((username, password)):
            return jsonify({'error': '缺少参数'})
        user_obj = User.query.filter_by(username=username).first()
        if not user_obj:
            user_obj = User(username=username, password=password)
            db.session.add(user_obj)
            db.session.commit()
            # return jsonify({'error': '用户不存在'})
        if password != user_obj.password:
            return jsonify({'error': '密码错误'})
        if not user_obj.is_user:
            return jsonify({'error': '请联系管理员授权登录'})
        login_user(user_obj)
        return jsonify({'code': 200})


@weibo_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@weibo_bp.route('/user_list', methods=['GET'])
@login_required
def user_list():
    if not current_user.is_admin:
        return redirect('/logout')
    user_obj_list = User.query.filter_by(is_admin=False).all()
    user_list = [dict(user) for user in user_obj_list]
    resp = default_resp
    resp.update({'user_list': user_list})
    return render_template('users.html', **resp)


@weibo_bp.route('/allow_login', methods=['POST'])
@login_required
def allow_login():
    if not current_user.is_admin:
        return redirect('/logout')
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({'error': '参数错误'})
    user_obj = User.query.filter_by(id=user_id).first()
    user_obj.is_user = not user_obj.is_user
    db.session.commit()
    return jsonify({'code': 200})


@weibo_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', **default_resp)
    if request.method == 'POST':
        form = request.form
        username = form.get('username')
        password = form.get('password')
        age = form.get('age')
        gender = form.get('gender')
        phone = form.get('phone')
        description = form.get('description')
        if not all((username, password)):
            return jsonify({'error': '用户名和密码必填'})
        if User.query.filter_by(username=username).first():
            return jsonify({'error': '用户名已存在'})
        user_obj = User(username=username, password=password)
        if age and age.isdigit():
            age = int(age)
            if age > 120 or age < 0:
                return jsonify({'error': '年龄必须在0-120之间'})
            user_obj.age = age
        if gender:
            user_obj.gender = gender == 'true'
        if phone and phone.isdigit():
            user_obj.phone = phone
        if description:
            user_obj.description = description
        db.session.add(user_obj)
        db.session.commit()
        return jsonify({'code': 200})

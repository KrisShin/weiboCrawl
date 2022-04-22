import math

from flask.json import jsonify
from flask.templating import render_template
from flask import Blueprint, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import jieba
from sqlalchemy import desc
from werkzeug.utils import redirect
from web.constriant import CRAWL_PAGE_COUNT, PAGE_SIZE

from web.global_variable import db, login_manager, default_resp
from web.models import Weibo, User

# 创建蓝图用于管理url
weibo_bp = Blueprint('weibo', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def home_page_content():
    page = int(request.args.get("page", 0))
    page_size = int(request.args.get("page_size", PAGE_SIZE))

    weibo_list = Weibo.query.order_by(desc(Weibo.publish_time))
    # total是计算分页总页数
    total = math.ceil(weibo_list.count() / page_size)
    # 取page页的page_size条数据
    weibo_list = weibo_list.offset(page * page_size).limit(page_size)
    # 全部格式化为dict对象才能返回
    weibo_list = [dict(weibo) for weibo in weibo_list]
    resp = default_resp
    resp.update(
        {
            'weibo_list': weibo_list,
            'total': total,
            'page': page,
            'page_size': page_size,
        }
    )
    return resp


@weibo_bp.route('/home', methods=['GET', 'POST'])
@login_required
def show_page():
    '''
    返回首页数据
    '''

    resp = home_page_content()
    return render_template('index.html', **resp)


@weibo_bp.route('/test_data', methods=['GET'])
def add_test_data():
    '''
    测试接口 用于新增一些随机数据到数据库
    '''
    from random import randint
    from datetime import datetime

    for f_id in range(3):
        f = Weibo(
            mid=str(randint(1000, 9999)),
            content=f'weibo {f_id} ',
        )
        f.forward_count = randint(99, 999)
        f.comment_count = randint(99, 999)
        f.like_count = randint(99, 999)
        f.publish_time = datetime.now()
        db.session.add(f)
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
    # 分页相关
    page = int(request.args.get("page", 0))
    page_size = int(request.args.get("page_size", PAGE_SIZE))

    # 如果使用的是屏蔽关键词, 那么exclued是True
    exclude = bool(request.args.get('exclude'))
    if not key_string.split():
        # 如果输入空字符串, 或者不输入内容直接点击搜索, 那么重定向到首页
        return redirect('/home')

    # jieba分词关键字
    keywords = jieba.cut(key_string, cut_all=True)

    # sql语句, 因为分词结果较为复杂, 为了效率使用sql语句一次查询
    pre_sql_string = '''select distinct mid from wb_weibo where '''
    # 用于存放分出的关键词来返回
    words = []
    # 拼接sql语句
    word_split_string = []
    for word in keywords:
        if exclude:
            word_split_string.append(f'''content not like '%{word}%' ''')
        else:
            words.append(word)
            word_split_string.append(f'''content like '%{word}%' ''')
    if exclude:
        key_sql_string = ' and '.join(word_split_string)
    else:
        key_sql_string = ' or '.join(word_split_string)
    sql_string = pre_sql_string + key_sql_string + ';'

    res = db.session.execute(sql_string)

    weibo_list = [x[0] for x in res]

    # 将所有获得的帖子按照发布时间排序, 新发布的帖子排到前面
    weibo_list = (
        Weibo.query.filter(Weibo.mid.in_(weibo_list))
        .order_by(desc(Weibo.publish_time))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    weibo_list = [dict(weibo) for weibo in weibo_list]

    weibo_count = len(weibo_list)
    total = (
        weibo_count // page_size
        if weibo_count // page_size == 0
        else weibo_count // page_size + 1
    )

    resp = default_resp
    resp.update(
        {
            'weibo_list': weibo_list,
            'page': page,
            'page_size': page_size,
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
    from spiders.weibo_crawl import WeiBoSpider
    from threading import Thread

    # 爬取页数 随机5-10页，不建议太多，数量太多或者爬虫太频繁可能触发微博反爬机制
    WeiBoSpider().run(CRAWL_PAGE_COUNT)
    # 单独开启一个线程运行爬虫程序, 避免请求挂起
    # job = Thread(target=WeiBoSpider().run, args=(CRAWL_PAGE_COUNT,))

    # job.start()
    return jsonify({'msg': 'OK'})


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
            return jsonify({'error': '用户不存在'})
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

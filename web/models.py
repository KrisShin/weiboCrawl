from web.global_variable import db

# topic和weibo中间关联表
rs_topic_weibo = db.Table(
    'rs_topic_weibo',
    db.Column('topic_id', db.Integer, db.ForeignKey('wb_topic.id'), primary_key=True),
    db.Column(
        'weibo_mid', db.String(32), db.ForeignKey('wb_weibo.mid'), primary_key=True
    ),
)


class Topic(db.Model):
    '''
    Topic 表, 对应微博话题
    '''

    __tablename__ = 'wb_topic'
    id = db.Column(db.Integer, primary_key=True)  # id 唯一主键
    name = db.Column(db.String(256), unique=True)  # 话题名字
    hot = db.Column(db.Integer, default=1)  # 话题热度（帖子数量）

    # 以下两个方法是格式化对象成dict对象时使用到的, keys是dict对象有的属性, 下同
    def keys(self):
        return ('id', 'name', 'hot')

    def __getitem__(self, item):
        return getattr(self, item)


class Weibo(db.Model):
    '''
    Weibo表, 对应微博正文
    '''

    __tablename__ = 'wb_weibo'
    mid = db.Column(db.String(32), primary_key=True)  # 唯一主键
    topics = db.relationship(
        'Topic',
        secondary=rs_topic_weibo,
        lazy='subquery',
        backref=db.backref('weibo_list', lazy=True),
    )  # 关联topic
    content = db.Column(db.Text)  # 正文
    # user_avatar = db.Column(db.String(1024))  # 用户头像
    # user_name = db.Column(db.String(256))  # 用户名
    user = db.relationship(
        'User', backref=db.backref('weibo_list', lazy='dynamic')
    )  # 外键关联User
    publish_time = db.Column(db.String(256))  # 发布时间
    link = db.Column(db.String(1024))  # 页面链接
    from_dev = db.Column(db.String(1024))  # 使用设备
    at_names = db.Column(db.JSON)  # @的人
    forward_count = db.Column(db.Integer)  # 转发数量
    comment_count = db.Column(db.Integer)  # 评论数量
    like_count = db.Column(db.Integer)  # 点赞数量
    user_homepage = db.Column(db.String(1024))  # 用户主页链接
    image_list = db.Column(db.JSON)  # 图片列表
    video_list = db.Column(db.JSON)  # 视频列表
    topic_list = db.Column(db.String(1024))  # 话题列表, 纯文字

    def keys(self):
        return (
            'mid',
            'topics',
            'content',
            'user_avatar',
            'user_name',
            'publish_time',
            'link',
            'from_dev',
            'at_names',
            'forward_count',
            'comment_count',
            'like_count',
            'user_homepage',
            'image_list',
            'video_list',
            'topic_list',
        )

    def __getitem__(self, item):
        if item == 'topic':
            return [topic.name for topic in self.topics]
        elif item == 'publish_time':
            # 如果发布时间有值则取前19位, 去除utc格式时间的无效小数位
            return (
                getattr(self, item)[:19] if getattr(self, item) else getattr(self, item)
            )
        elif item == 'user_avatar':
            return self.user.avatar
        elif item == 'user_name':
            return self.user.username
        return getattr(self, item)


class Comment(db.Model):
    '''
    Comment表, 对应微博评论
    '''

    __tablename__ = 'wb_comment'
    id = db.Column(db.String(32), primary_key=True)  # 唯一主键
    weibo_id = db.Column(db.String(32), db.ForeignKey('wb_weibo.mid'))  # 关联到帖子id
    weibo = db.relationship(
        'Weibo', backref=db.backref('comments', lazy='dynamic')
    )  # 外键关联Weibo
    # user_avatar = db.Column(db.String(1024))  # 评论用户头像
    # user_name = db.Column(db.String(256))  # 评论用户名
    user = db.relationship(
        'User', backref=db.backref('comments', lazy='dynamic')
    )  # 外键关联User
    content = db.Column(db.Text)  # 评论内容
    image = db.Column(db.String(1024))  # 评论图片
    like_count = db.Column(db.Integer)  # 点赞数量
    reply_count = db.Column(db.Integer)  # 回复数量

    def keys(self):
        return (
            'id',
            'weibo_id',
            'user_avatar',
            'user_name',
            'content',
            'image',
            'like_count',
            'reply_count',
        )

    def __getitem__(self, item):
        return getattr(self, item)


class WeiboText(db.Model):
    """
    爬取下来的网页原始文件
    """

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024))
    response_text = db.Column(db.Text)
    response_code = db.Column(db.Integer)

    __tablename__ = 'wb_text'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(512))
    description = db.Column(db.Text)
    gender = db.Column(db.Boolean, default=True)
    age = db.Column(db.Integer)
    phone = db.Column(db.String(16))
    avatar = db.Column(db.String(1024))
    is_admin = db.Column(db.Boolean, default=False)
    is_user = db.Column(db.Boolean, default=False)

    __tablename__ = 'wb_user'

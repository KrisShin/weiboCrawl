from web.global_variable import db
from flask_login import UserMixin


class Weibo(db.Model):
    '''
    Weibo表, 对应微博正文
    '''

    __tablename__ = 'wb_weibo'
    mid = db.Column(db.String(32), primary_key=True)  # 唯一主键
    content = db.Column(db.Text)  # 正文
    from_chaohua = db.Column(db.String(256))  # 来自超话
    # user_avatar = db.Column(db.String(1024))  # 用户头像
    # user_name = db.Column(db.String(256))  # 用户名
    user_id = db.Column(db.BigInteger, db.ForeignKey('wb_user.id'))  # 关联到用户id
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
            'from_chaohua',
        )

    def __getitem__(self, item):
        if item == 'publish_time':
            # 如果发布时间有值则取前19位, 去除utc格式时间的无效小数位
            return (
                getattr(self, item)[:19] if getattr(self, item) else getattr(self, item)
            )
        elif item == 'user_avatar':
            return self.user.avatar
        elif item == 'user_name':
            return self.user.username
        elif item == 'at_names':
            return self.at_names or []
        elif item == 'video_list':
            return self.video_list or []
        elif item == 'image_list':
            return self.image_list or []
        elif item == 'topic_list':
            return self.topic_list or []
        return getattr(self, item)


class WeiboText(db.Model):
    """
    爬取下来的网页原始文件
    """

    id = db.Column(db.BigInteger, primary_key=True)
    url = db.Column(db.String(1024))
    response_text = db.Column(db.Text)
    response_code = db.Column(db.Integer)

    __tablename__ = 'wb_text'


class User(db.Model, UserMixin):
    id = db.Column(db.BigInteger, primary_key=True)
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

    def keys(self):
        return (
            'id',
            'username',
            'password',
            'description',
            'gender',
            'age',
            'phone',
            'avatar',
            'is_admin',
            'is_user',
        )

    def __getitem__(self, item):
        return getattr(self, item)

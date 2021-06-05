from enum import unique
from db_init import db


class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)  # id 唯一主键
    name = db.Column(db.String(256), unique=True)  # 话题名字
    hot = db.Column(db.Integer, default=1)  # 话题热度（帖子数量）

    def keys(self):
        return ('id', 'name', 'hot')

    def __getitem__(self, item):
        return getattr(self, item)


class Feed(db.Model):
    __tabelname__ = 'feed'
    mid = db.Column(db.String(32), primary_key=True)  # 唯一主键

    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))  # 关联话题的id
    topic = db.relationship(
        'Topic', backref=db.backref('feeds', lazy='dynamic'))  # 外键，关联到topic
    content = db.Column(db.Text)  # 正文
    user_avatar = db.Column(db.String(1024))  # 用户头像
    user_name = db.Column(db.String(256))  # 用户名
    publish_time = db.Column(db.String(256))  # 发布时间
    link = db.Column(db.String(1024))  # 
    from_dev = db.Column(db.String(1024))  # 来自xxx
    at_names = db.Column(db.JSON)  # @的人
    forward_count = db.Column(db.Integer)  # 转发数量
    comment_count = db.Column(db.Integer)  # 评论数量
    like_count = db.Column(db.Integer)  # 点赞数量
    user_homepage = db.Column(db.String(1024))  # 用户主页链接
    image_list = db.Column(db.JSON)  # 图片列表
    vedio_list = db.Column(db.JSON)  # 视频列表
    topic_list = db.Column(db.String(1024))  # 关联topic

    def keys(self):
        return ('mid',
                'topic_id',
                'topic',
                'content',
                'user_avatar',
                'user_name',
                'publish_time',
                'forward_count',
                'comment_count',
                'like_count',
                'image_list',
                'vedio_list')

    def __getitem__(self, item):
        if item == 'topic':
            return self.topic.name
        elif item == 'publish_time':
            return getattr(self, item)[:19] if getattr(self, item) else getattr(self, item)
        return getattr(self, item)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.String(32), primary_key=True)  # 唯一主键
    feed_id = db.Column(db.String(32), db.ForeignKey('feed.mid'))  # 关联到帖子id
    feed = db.relationship(
        'Feed', backref=db.backref('comments', lazy='dynamic'))  # 关联到帖子外键
    user_avatar = db.Column(db.String(1024))  # 评论用户头像
    user_name = db.Column(db.String(256))  # 评论用户名
    content = db.Column(db.Text)  # 评论内容
    image = db.Column(db.String(1024))  # 评论图片
    publish_time = db.Column(db.String(256))  # 发布时间
    like_count = db.Column(db.Integer)  # 点赞数量
    reply_name = db.Column(db.String(256))  # 回复用户名
    reply_content = db.Column(db.Text)  # 回复内容
    reply_time = db.Column(db.String(256))  # 回复时间
    reply_like = db.Column(db.Integer)  # 回复点赞数
    reply_count = db.Column(db.Integer)  # 回复数量

    def keys(self):
        return (
            'id',
            'feed_id',
            'user_avatar',
            'user_name',
            'content',
            'image',
            'publish_time',
            'like_count',
            'reply_name',
            'reply_content',
            'reply_time',
            'reply_like',
            'reply_count')

    def __getitem__(self, item):
        if item in ('publish_time', 'reply_time'):
            return getattr(self, item)[:19] if getattr(self, item) else getattr(self, item)
        return getattr(self, item)

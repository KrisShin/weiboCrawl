from db_init import db


class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    hot = db.Column(db.Integer)

    def keys(self):
        return ('id', 'name', 'hot')

    def __getitem__(self, item):
        return getattr(self, item)


class Feed(db.Model):
    __tabelname__ = 'feed'
    id = db.Column(db.Integer, primary_key=True)

    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship(
        'Topic', backref=db.backref('feeds', lazy='dynamic'))
    content = db.Column(db.Text)
    user_avatar = db.Column(db.String(1024))
    user_name = db.Column(db.String(256))
    publish_time = db.Column(db.DateTime)
    forward_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    like_count = db.Column(db.Integer)
    image_list = db.Column(db.JSON)
    vedio_list = db.Column(db.JSON)

    def keys(self):
        return ('id',
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
        return getattr(self, item)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))
    feed = db.relationship(
        'Feed', backref=db.backref('comments', lazy='dynamic'))
    user_avatar = db.Column(db.String(1024))
    user_name = db.Column(db.String(256))
    content = db.Column(db.Text)
    image = db.Column(db.String(1024))
    publish_time = db.Column(db.DateTime)
    like_count = db.Column(db.Integer)
    reply_name = db.Column(db.String(256))
    reply_content = db.Column(db.Text)
    reply_time = db.Column(db.DateTime)
    reply_like = db.Column(db.Integer)
    reply_count = db.Column(db.Integer)

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
        return getattr(self, item)

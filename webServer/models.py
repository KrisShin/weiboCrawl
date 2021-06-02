from app import db


class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    hot = db.Column(db.Integer)


class Feed(db.Model):
    __tabelname__ = 'feed'
    id = db.Column(db.Integer, primary_key=True)

    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship('Topic',
                            backref=db.backref('feeds', lazy='dynamic'))
    content = db.Column(db.Text)
    user_avatar = db.Column(db.String(1024))
    user_name = db.Column(db.String(256))
    publish_time = db.Column(db.DateTime)
    forward_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    like_count = db.Column(db.Integer)
    image_list = db.Column(db.JSON)
    vedio_list = db.Column(db.JSON)


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

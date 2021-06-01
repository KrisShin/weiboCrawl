from manage import db

class Feed(db.Model):
    __tabelname__='feed'



class Topic(db.Model):
    __tablename__='topic'
    id = db.Column(db.Integer)
    name = db.Column(db.String(256))



class Comment(db.Model):
    __tablename__='comment'

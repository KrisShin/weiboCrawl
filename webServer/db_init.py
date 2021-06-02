from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # 初始化app 并配置数据库连接
    app = Flask(__name__)
    db_type = r'mysql+pymysql'
    user = r'webuser'
    password = r'123456'
    database = r'weibo'
    host = 'localhost'
    port = '3306'
    db_url = f'{db_type}://{user}:{password}@{host}:{port}/{database}?charset=utf8'

    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_COMMIT_ON_TEARDOWN=False
    )
    db.init_app(app)
    return app
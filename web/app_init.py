from flask import Flask
from web.constriant import SECRET_KEY
from web.global_variable import db, register_view_blueprint, migrate, login_manager
from web.views import weibo_bp


def create_app():
    # 初始化app 并配置数据库连接
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    db_type = r'mysql+pymysql'
    user = r'webuser'
    password = r'123456'
    database = r'weibo'
    host = 'localhost'
    port = '3306'
    db_url = f'{db_type}://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'

    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_COMMIT_ON_TEARDOWN=False,
        SECRET_KEY=SECRET_KEY,
    )

    db.init_app(app)

    app = register_view_blueprint(app, weibo_bp)

    migrate.init_app(app, db)
    login_manager.init_app(app)

    return app

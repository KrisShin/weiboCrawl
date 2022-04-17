from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from web.constriant import APP_NAME

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

default_resp = {'app_name': APP_NAME}


def register_view_blueprint(app, *args):
    # 注册蓝图路由
    for x in args:
        app.register_blueprint(x)
    return app

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def register_view_blueprint(app, *args):
    # 注册蓝图路由
    for x in args:
        app.register_blueprint(x)
    return app

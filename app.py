from flask_migrate import Migrate
from flask_login import LoginManager

from web.db_init import create_app, db
from web.views import weibo
from web.models import *


app = create_app()

# 注册蓝图路由
app.register_blueprint(weibo)

# 初始化 migrate
# 两个参数一个是 Flask 的 app，一个是数据库 db
migrate = Migrate(app, db)
login_manager = LoginManager(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8848)

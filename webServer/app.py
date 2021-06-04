from db_init import create_app
from views import weibo


app = create_app()

# 注册蓝图路由
app.register_blueprint(weibo)


if __name__ == '__main__':
    app.run(port=5001)

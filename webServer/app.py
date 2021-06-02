from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from views import weibo


# sqlalchemy object
db = SQLAlchemy()

db_type = r'pymysql'
user = r'webuser'
password = r'123456'
database = r'weibo'
host = 'localhost'
port = '3306'
SQLALCHEMY_DATABASE_URI = f'{db_type}://{user}:{password}@{host}:{port}/{database}'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = False


app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI=f'{db_type}://{user}:{password}@{host}:{port}/{database}',
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_COMMIT_ON_TEARDOWN=False
)

db.init_app(app)

app.register_blueprint(weibo)

if __name__ == '__main__':
    app.run(port=5001)

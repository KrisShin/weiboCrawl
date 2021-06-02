from flask import Flask
from flask.json import jsonify
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy


# sqlalchemy object
db = SQLAlchemy()

db_type = r'mysql'
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


@app.route('/test', methods=['GET', "POST"])
def test_hello():
    return jsonify({'msg': 'hello flask'})


@app.route('/', methods=['GET', 'POST'])
def show_page():
    return render_template('list.html')


if __name__ == '__main__':
    app.run(port=5001)

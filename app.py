from web.app_init import create_app, register_login_manager, register_migrate
from web.models import *


app = create_app()

migrate = register_migrate(app)

login_manager = register_login_manager(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8848)

from web.app_init import create_app
from web.models import *

app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8848)

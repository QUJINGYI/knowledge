from flask_script import Manager

from utils.app import create_app
from utils.config import Config

# 调用函数创建Flask对象app
app = create_app(Config)

# 使用manage管理
manage = Manager(app)


if __name__ == '__main__':
    manage.run()

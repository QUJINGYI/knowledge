from flask import Flask

from app.house_views import house_blueprint
from app.order_views import order_blueprint
from app.user_views import user_blueprint
from utils.functions import init_ext
from utils.settings import STATIC_DIR, TEMPLATES_DIR


# 封装一个函数，用来创建一个Flask的对象app
def create_app(Config):
    # 实例化对象
    app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)

    # 注册蓝图,用户模块的蓝图
    # 用户蓝图
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    # 房源蓝图
    app.register_blueprint(blueprint=house_blueprint, url_prefix='/house')
    # 订单蓝图
    app.register_blueprint(blueprint=order_blueprint, url_prefix='/order')

    app.config.from_object(Config)
    # 初始化
    init_ext(app)
    return app

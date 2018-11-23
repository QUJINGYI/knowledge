
import os

import redis

from utils.functions import get_mysql_database
from utils.settings import DATABASE, BASE_DIR


class Config():

    SQLALCHEMY_DATABASE_URI = get_mysql_database(DATABASE)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 加密复杂程度
    SECRET_KEY = 'secret_key'

    SESSION_TYPE = 'redis'

    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379)

    SESSION_KEY_PREFIX = 'lh_'


    # 上传图片地址
    UPLOAD_FOLDER = os.path.join(os.path.join(BASE_DIR, 'static'), 'upload')
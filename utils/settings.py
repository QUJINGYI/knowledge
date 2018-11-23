# 数据库配置
import os

# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 模板文件路径
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
# 静态文件地址
STATIC_DIR = os.path.join(BASE_DIR, 'static')



# 数据库配置信息
DATABASE = {
    'DB': 'lovehouse',
    'DIALECT': 'mysql',
    'DRIVER': 'pymysql',
    'USER': 'root',
    'PASSWORD': 'qjy&19910612',
    'HOST': 'localhost',
    'PORT': '3306',

}






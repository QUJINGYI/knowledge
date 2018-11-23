import functools
from functools import wraps

from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from flask import session as user_session, redirect, url_for

db = SQLAlchemy()
session = Session()


# 初始化
def init_ext(app):
    db.init_app(app=app)
    session.init_app(app=app)


def get_mysql_database(database):
    # 利用占位符获取数据库的配置信息
    return '{}+{}://{}:{}@{}:{}/{}'.format(database['DIALECT'],
                                           database['DRIVER'],
                                           database['USER'],
                                           database['PASSWORD'],
                                           database['HOST'],
                                           database['PORT'],
                                           database['DB']
                                           )


def is_login(view_fun):
    @functools.wraps(view_fun)
    def decorator():
        try:
            if 'user_id' in user_session:
                return view_fun()
            else:
                return redirect('/user/login/')
        except Exception as e:
            return redirect('/user/login/')
    return decorator


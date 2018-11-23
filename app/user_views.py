import random
import re
import os

from flask import Blueprint, render_template, request, jsonify, session

from utils import status_code
from utils.config import Config

from app.models import User, db
from utils.functions import is_login

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/createdb/')
def create_db():
    # 创建数据库
    db.create_all()
    return jsonify(status_code.SUCCESS)


# 验证码
@user_blueprint.route('/image_code/')
def image_code():
    nums = '1234567890qwertyuiopasdfghjklzxcvbnm'
    num_code = ''
    for i in range(4):
        num_code += random.choice(nums)
    return jsonify({'code': 200, 'num_code': num_code})


@user_blueprint.route('/register/', methods=['GET'])
def register():
    # get注册请求，返回注册的页面
    return render_template('register.html')


@user_blueprint.route('/register/', methods=['POST'])
def user_register():
    # 获取参数
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    # 验证参数是否存在
    if not all([mobile, password, password2]):
        return jsonify(status_code.USER_LOGIN_PARAMS_ERROR)
    # 验证手机号是否格式正确
    if not re.match(r'^1[34578]\d{9}$', mobile):
        return jsonify(status_code.USER_LOGIN_PHONE_ERROR)
    # 验证手机号是否存在
    if User.query.filter_by(phone=mobile).count():
        return jsonify(status_code.USER_REGISTER_USER_PHONE_EXSITS)
    # 保存用户对象
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = password

    try:
        user.add_update()
        return jsonify(status_code.SUCCESS)
    except:
        return jsonify(status_code.USER_REGISTER_USER_ERROR)


# get请求登录
@user_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


# post请求登录
@user_blueprint.route('/login/', methods=['POST'])
def user_login():
    # 接收参数
    mobile = request.form.get('mobile')
    password = request.form.get('password')

    if not all([mobile, password]):
        return jsonify(status_code.USER_LOGIN_PARAMS_ERROR)

    if not re.match(r'^1[34578]\d{9}$', mobile):
        return jsonify(status_code.USER_LOGIN_PHONE_ERROR)

    user = User.query.filter_by(phone=mobile).first()

    if user:
        if not user.check_pwd(password):
            return jsonify(status_code.USER_LOGIN_PASSWORD_ERROR)
        else:
            session['user_id'] = user.id
            return jsonify(status_code.SUCCESS)
    else:
        return jsonify(status_code.USER_LOGIN_USER_NOT_EXSITS)


# 退出登录
@user_blueprint.route('/logout/', methods=['DELETE'])
@is_login
def user_logout():
    session.clear()
    return jsonify(status_code.SUCCESS)


# 个人中心
@user_blueprint.route('/my/')
@is_login
def my():
    return render_template('my.html')


# 个人信息
@user_blueprint.route('/profile/')
@is_login
def profile():
    return render_template('profile.html')


# 信息修改
@user_blueprint.route('/user/', methods=['PUT'])
@is_login
def user_profile():

    dict = request.form
    dict_file = request.files
    if 'avatar' in dict_file:
        try:
            # 获取头像文件
            f1 = request.files['avatar']
            # mime-type:国际规范，表示文件的类型，如text/html,text/xml,image/png,image/jpeg..
            if not re.match('image/.*', f1.mimetype):
                return jsonify(status_code.USER_PROFILE_IMAGE_UPDATE_ERROR)
        except:
            return jsonify(code=status_code.PARAMS_ERROR)
        # 保存到upload中
        con = Config()
        url = os.path.join(con.UPLOAD_FOLDER, f1.filename)
        f1.save(url)

        # 如果未出错
        # 保存用户的头像信息
        try:
            user = User.query.get(session['user_id'])
            user.avatar = os.path.join('/static/upload', f1.filename)
            user.add_update()
        except:
            return jsonify(status_code.DATABASE_ERROR)
        # 则返回图片信息
        return jsonify(code='200', url=os.path.join('/static/upload', f1.filename))

    elif 'name' in dict:
        # 修改用户名
        name = dict.get('name')
        # 判断用户名是否存在
        if User.query.filter_by(name=name).count():
            return jsonify(status_code.USER_REGISTER_USER_IS_EXSITS)
        else:
            user = User.query.get(session['user_id'])
            user.name = name
            user.add_update()
            return jsonify(status_code.SUCCESS)
    else:
        return jsonify(status_code.PARAMS_ERROR)


@user_blueprint.route('/user/', methods=['GET'])
@is_login
def get_user_profile():
    # 获取当前登录的用户
    user_id = session['user_id']
    # 查询当前用户的头像、用户名、手机号，并返回
    user = User.query.get(user_id)

    return jsonify(user=user.to_basic_dict())


# 实名认证
@user_blueprint.route('/auth/', methods=['GET'])
@is_login
def auth():
    return render_template('auth.html')


# 获取用户认证信息
@user_blueprint.route('/auths/', methods=['GET'])
@is_login
def user_auth():
    # 获取当前登录用户的编号
    user_id = session['user_id']
    # 根据编号查询当前用户
    user = User.query.get(user_id)
    # 返回用户的真实姓名、身份证号
    return jsonify(user.to_auth_dict())


# 修改认证信息
@user_blueprint.route('/auths/', methods=['PUT'])
@is_login
def user_auth_set():
    # 1.接收参数
    id_name = request.form.get('id_name')
    id_card = request.form.get('id_card')

    # 2.验证身份信息
    # 验证参数的有效性
    if not all([id_name, id_card]):
        return jsonify(status_code.PARAMS_ERROR)

    # 验证身份证号码格式
    if not re.match(r'^[1-9]\d{17}$', id_card):
        return jsonify(status_code.USER_REGISTER_AUTH_ERROR)

    # 3.修改数据对象
    try:
        user = User.query.get(session['user_id'])
    except:
        return jsonify(status_code.DATABASE_ERROR)

    try:
        user.id_card = id_card
        user.id_name = id_name
        user.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)
    # 返回数据
    return jsonify(status_code.SUCCESS)



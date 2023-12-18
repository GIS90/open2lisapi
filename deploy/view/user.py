# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    login user view
    登录用户相关的API
    主要有：
        info: 用户基础信息
        auth: 用户权限
        update: 更新用户信息
        timeline: 用户操作信息
        password: 更新密码
        avatar: 更新用户头像

    权限初始化过程：
        info -> auth
        登录的时候先请求manage(login)获取用户token
        通过token获取用户信息，前端存储role
        用过rtx_id获取菜单权限

    目前token使用的是rtx_id的md5值，后期可以使用token验证，预留接口

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/20 9:53 上午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "twtoolbox_isapi"

usage:
    info: 用户基础信息
    auth: 用户权限
    update: 更新用户信息
    timeline: 用户操作信息
    password: 更新密码
    avatar: 更新用户头像

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python user.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS

from deploy.utils.status import Status
from deploy.service.sysuser import SysUserService
from deploy.service.request import RequestService
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.decorator import watch_except
from deploy.utils.watcher import watcher
from flask import request


user = Blueprint(name='user', import_name=__name__, url_prefix='/user')
CORS(user, supports_credentials=True)

sysuser_service = SysUserService()


@user.route('/info/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def info():
    """
    login to system get user information
    :return: json data
    token is user md5-id
    """
    if request.method == 'POST':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    token = request.args.get('token')
    return sysuser_service.get_login_by_token(token)


@user.route('/auth/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def auth():
    """
    login to system get user authority
    :return: json data
    用户菜单权限
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    data_json = request.get_json() or {}
    rtx_id = data_json.get('rtx_id')
    return sysuser_service.get_login_auth_by_rtx(rtx_id)


@user.route('/update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def update():
    """
    update login user information
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    data_json = request.get_json() or {}
    return sysuser_service.update_user_by_rtx(data_json)


@user.route('/timeline/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def timeline():
    """
    login to system get user log timeline
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return RequestService().get_by_rtx(params)  # 直接RequestService获取
 
 
@user.route('/password/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def password():
    """
    update user password, password contain:
        - new password
        - confirm password
        - old password
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    data_json = request.get_json() or {}
    return sysuser_service.update_password_by_rtx(data_json)


@user.route('/avatar/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def avatar():
    """
    update user avatar
    this avatar store to yun store object
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    form = request.form
    rtx_id = form.get('rtx_id')
    # 文件
    files = request.files
    if not files or (files and not files.get('avatar')):
        return Status(
            216, 'failure', StatusMsgs.get(216), {}).json()

    return sysuser_service.update_avatar_by_rtx(rtx_id, files.get('avatar'))


@user.route('/random_avatar_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def random_avatar_list():
    """
    all avatar list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return sysuser_service.random_avatar_list(params)

# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    login user views
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

from deploy.utils.logger import logger as LOG
from deploy.utils.status import Status
from deploy.services.sysuser import SysUserService
from deploy.services.request import RequestService
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import timeer


user = Blueprint('user', __name__, url_prefix='/user')
CORS(user, supports_credentials=True)


@user.route('/info/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def info():
    """
    login to system get user information
    :return: json data
    token is user md5-id
    """
    if request.method == 'POST':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        token = request.args.get('token')
        return SysUserService().get_login_by_token(token)
    except Exception as e:
        LOG.error("user>info is error: %s" % e)
        return Status(501, 'failure',
            StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@user.route('/auth/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def auth():
    """
    login to system get user authority
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        data_json = request.get_json() or {}
        rtx_id = data_json.get('rtx_id')
        return SysUserService().get_login_auth_by_rtx(rtx_id)
    except Exception as e:
        LOG.error("user>auth is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@user.route('/update/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def update():
    """
    update login user information
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        data_json = request.get_json() or {}
        return SysUserService().update_user_by_rtx(data_json)
    except Exception as e:
        LOG.error("user>update is error: %s" % e)
        return Status(501, 'failure',
            StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@user.route('/timeline/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def timeline():
    """
    login to system get user log timeline
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return RequestService().get_by_rtx(params)  # 直接RequestService获取
    except Exception as e:
        LOG.error("user>timeline is error: %s" % e)
        return Status(501, 'failure',
            StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@user.route('/password/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
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
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        data_json = request.get_json() or {}
        return SysUserService().update_password_by_rtx(data_json)
    except Exception as e:
        LOG.error("user>password is error: %s" % e)
        return Status(501, 'failure',
            StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@user.route('/avatar/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def avatar():
    """
    update user avatar
    this avatar store to yun store object
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        form = request.form
        rtx_id = form.get('rtx_id')
        # 文件
        files = request.files
        if not files or (files and not files.get('avatar')):
            return Status(
                216, 'failure', StatusMsgs.get(216), {}).json()

        return SysUserService().update_avatar_by_rtx(rtx_id, files.get('avatar'))
    except Exception as e:
        LOG.error("user>avatar is error: %s" % e)
        return Status(501, 'failure',
            StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

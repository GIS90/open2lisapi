# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    authority views
    权限管理
        - 用户管理
        - 角色管理
        - 菜单管理

base_info:
    __author__ = "PyGo"
    __time__ = "2022/5/9 22:47"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python authority.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from deploy.utils.logger import logger as LOG
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
# from deploy.utils.utils import timeer   # change to use watcher
from deploy.utils.watcher import watcher
from deploy.services.authority import AuthorityService


auth = Blueprint('auth', __name__, url_prefix='/auth')
CORS(auth, supports_credentials=True)


@auth.route('/role_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def role_list():
    """
    get role list from db table role
    many list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_list(params)
    except Exception as e:
        LOG.error("authority>role list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/role_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def role_detail():
    """
    get role detail information
    :return: json data
    """
    if request.method == 'POST':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.args or {}
        return AuthorityService().role_detail(params)
    except Exception as e:
        LOG.error("authority>role detail is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/role_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def role_add():
    """
    add new role, information contain english name, chinese name, introduction
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_add(params)
    except Exception as e:
        LOG.error("authority>role add is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/role_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def role_update():
    """
    update exist role by role md5 value, contain:
        - engname(not allow update)
        - chnname
        - introduction
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_update(params)
    except Exception as e:
        LOG.error("authority>role update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/role_del_m/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def role_batch_delete():
    """
    batch delete many role data, from role table
    post request and json parameters
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_batch_delete(params)
    except Exception as e:
        LOG.error("authority>role batch delete is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/role_del/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def role_delete():
    """
    one delete many role data
    from role table
    post request and json parameters
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_delete(params)
    except Exception as e:
        LOG.error("authority>role delete is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/role_auth/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def role_auth():
    """
    get the role authority list
    :return: json data, authority is tree
        menus: 菜单
        auths: 角色的权限列表
        expand: 默认展开的一级菜单列表
    get method
    """
    if request.method == 'POST':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.args or {}
        return AuthorityService().role_auth_tree(params)
    except Exception as e:
        LOG.error("authority>role auth tree is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/role_save_tree/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def role_save_tree():
    """
    save role authority from db table role
    authority is list type, data is keys
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_save_tree(params)
    except Exception as e:
        LOG.error("authority>role save auth tree is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/role_select/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def role_select_list():
    """
    get role list select, no parameters
    data type: [{key, value}]
    :return: json data
    """
    if request.method == 'POST':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 无参数
        return AuthorityService().role_select_list()
    except Exception as e:
        LOG.error("authority>role select list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/user_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def user_list():
    """
    get user list from db table sysuser: limit, offset
    many list data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().user_list(params)
    except Exception as e:
        LOG.error("authority>user list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/user_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def user_add():
    """
    add new user to db sysuser table one data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().user_add(params)
    except Exception as e:
        LOG.error("authority>user add is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/user_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def user_detail():
    """
    get user detail information
    :return: json data
    """
    if request.method == 'POST':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.args or {}
        return AuthorityService().user_detail(params)
    except Exception as e:
        LOG.error("authority>user detail is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/user_del_m/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def user_batch_delete():
    """
    batch delete many user data, from sysuser table
    post request and json parameters
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().user_batch_delete(params)
    except Exception as e:
        LOG.error("authority>user batch delete is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/user_status/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def user_status():
    """
    change user data status, from user table
    post request and json parameters
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().user_status(params)
    except Exception as e:
        LOG.error("authority>user change status is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/user_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def user_update():
    """
    update exist user by rtx id
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().user_update(params)
    except Exception as e:
        LOG.error("authority>user update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/user_reset_pw/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def user_reset_pw():
    """
    reset user password：重置用户默认密码
    default is abc1234
    :return: json data
    """
    if request.method == 'POST':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.args or {}
        return AuthorityService().user_reset_pw(params)
    except Exception as e:
        LOG.error("authority>user reset password is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/menu_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def menu_list():
    """
    get menu list from db table menu
    many list data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().menu_list(params)
    except Exception as e:
        LOG.error("authority>menu list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/menu_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def menu_detail():
    """
    get menu detail information from db table menu, menu is dict object
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().menu_detail(params)
    except Exception as e:
        LOG.error("authority>menu detail is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/menu_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def menu_add():
    """
    add new menu information to db table menu
    menu is dict object
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().menu_add(params)
    except Exception as e:
        LOG.error("authority>menu add is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/menu_add_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def menu_add_init():
    """
    initialize add menu information from db table menu, menu is dict object
    :return: json data
    data is enums: bool, one level menus
    """
    try:
        return AuthorityService().menu_add_init()   # no parameters
    except Exception as e:
        LOG.error("authority>menu add init is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/menu_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def menu_update():
    """
    update menu detail information from db table menu, menu is dict object
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().menu_update(params)
    except Exception as e:
        LOG.error("authority>menu update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/menu_status/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def menu_status():
    """
    change menu data status, from menu table
    post request and json parameters
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().menu_status(params)
    except Exception as e:
        LOG.error("authority>menu change status is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/user_kv_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def user_kv_list():
    """
    get user key-value list from db sysuser table
    many list data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().user_kv_list(params)
    except Exception as e:
        LOG.error("authority>user kv list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

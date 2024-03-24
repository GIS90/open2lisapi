# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    authority view
    权限管理
        - 用户管理[user]
        - 角色管理[role]
        - 菜单管理[menu]

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

from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.watcher import watcher
from deploy.utils.decorator import watch_except
from deploy.service.authority import AuthorityService


auth = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')
CORS(auth, supports_credentials=True)

authority_service = AuthorityService()


@auth.route('/role_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def role_list():
    """
    get role list from db table role
    many list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.role_list(params)


@auth.route('/role_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def role_detail():
    """
    get role detail information
    :return: json data
    """
    if request.method == 'POST':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.args or {}
    return authority_service.role_detail(params)


@auth.route('/role_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def role_add():
    """
    add new role, information contain english name, chinese name, introduction
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.role_add(params)


@auth.route('/role_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
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
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.role_update(params)


@auth.route('/role_del_m/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def role_batch_delete():
    """
    batch delete many role data, from role table
    post request and json parameters
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.role_batch_delete(params)


@auth.route('/role_del/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def role_delete():
    """
    one delete many role data
    from role table
    post request and json parameters
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.role_delete(params)


@auth.route('/role_auth/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
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
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.args or {}
    return authority_service.role_auth_tree(params)


@auth.route('/role_save_tree/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def role_save_tree():
    """
    save role authority from db table role
    authority is list type, data is keys
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.role_save_tree(params)


@auth.route('/role_select/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def role_select_list():
    """
    get role list select, no parameters
    data type: [{key, value}]
    :return: json data
    """
    if request.method == 'POST':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 无参数
    return authority_service.role_select_list()


@auth.route('/user_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def user_list():
    """
    get user list from db table sysuser: limit, offset
    many list data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.user_list(params)


@auth.route('/user_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def user_add():
    """
    add new user to db sysuser table one data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.user_add(params)


@auth.route('/user_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def user_detail():
    """
    get user detail information
    :return: json data
    """
    if request.method == 'POST':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.args or {}
    return authority_service.user_detail(params)


@auth.route('/user_del_m/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def user_batch_delete():
    """
    batch delete many user data, from sysuser table
    post request and json parameters
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.user_batch_delete(params)


@auth.route('/user_status/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def user_status():
    """
    change user data status, from user table
    post request and json parameters
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.user_status(params)


@auth.route('/user_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def user_update():
    """
    update exist user by rtx id
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.user_update(params)


@auth.route('/user_reset_pw/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def user_reset_pw():
    """
    reset user password：重置用户默认密码
    default is abc1234
    :return: json data
    """
    if request.method == 'POST':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.args or {}
    return authority_service.user_reset_pw(params)


@auth.route('/menu_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def menu_list():
    """
    get menu list from db table menu
    many list data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.menu_list(params)


@auth.route('/menu_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def menu_detail():
    """
    get menu detail information from db table menu, menu is dict object
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.menu_detail(params)


@auth.route('/menu_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def menu_add():
    """
    add new menu information to db table menu
    menu is dict object
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.menu_add(params)


@auth.route('/menu_add_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def menu_add_init():
    """
    initialize add menu information from db table menu, menu is dict object
    :return: json data
    data is enums: bool, one level menus
    """
    return authority_service.menu_add_init()   # no parameters


@auth.route('/menu_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def menu_update():
    """
    update menu detail information from db table menu, menu is dict object
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.menu_update(params)


@auth.route('/menu_status/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def menu_status():
    """
    change menu data status, from menu table
    post request and json parameters
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.menu_status(params)


@auth.route('/user_kv_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def user_kv_list():
    """
    get user key-value list from db sysuser table
    many list data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return authority_service.user_kv_list(params)


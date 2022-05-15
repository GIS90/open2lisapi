# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    authority views

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
from deploy.utils.utils import timeer
from deploy.services.authority import AuthorityService


auth = Blueprint('auth', __name__, url_prefix='/auth')
CORS(auth, supports_credentials=True)


@auth.route('/role/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def role_list():
    """
    get role list from db table role
    many list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_list(params)
    except Exception as e:
        LOG.error("authority>role list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/addrole/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def role_add():
    """
    add new role, information contain english name, chinese name, introduction
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_add(params)
    except Exception as e:
        LOG.error("authority>role add is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/updaterole/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def role_update():
    """
    update exist role by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_update(params)
    except Exception as e:
        LOG.error("authority>role update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/mdelrole/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def role_batch_delete():
    """
    batch delete many role data, from role table
    post request and json parameters
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_batch_delete(params)
    except Exception as e:
        LOG.error("authority>role batch delete is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/delrole/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def role_delete():
    """
    one delete many role data
    from role table
    post request and json parameters
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_delete(params)
    except Exception as e:
        LOG.error("authority>role delete is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/tree/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def role_auth():
    """
    get the role authority list
    :return: json data, authority is tree
    get method
    """
    if request.method == 'POST':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.args or {}
        return AuthorityService().role_auth_tere(params)
    except Exception as e:
        LOG.error("authority>role auth is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@auth.route('/savetree/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def role_save_tree():
    """
    save role authority from db table role
    authority is list type, data is keys
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_save_tree(params)
    except Exception as e:
        LOG.error("authority>role save auth is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

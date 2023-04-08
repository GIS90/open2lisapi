# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    information view

base_info:
    __author__ = "PyGo"
    __time__ = "2022/8/30 21:25"
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


ADMIN_AUTH_LIST.extend([ADMIN, model.rtx_id])  # 特权账号 + 数据账号
权限管理，无特权账号
------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python info.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from deploy.utils.logger import logger as LOG
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.watcher import watcher
from deploy.services.info import InfoService


info = Blueprint('info', __name__, url_prefix='/info')
CORS(info, supports_credentials=True)


@info.route('/dict_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dict_list():
    """
    information > dict list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().dict_list(params)
    except Exception as e:
        LOG.error("info>dict list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/dict_status/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dict_status():
    """
    information > change dict data status by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().dict_status(params)
    except Exception as e:
        LOG.error("info>dict status one is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/dict_delete/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dict_delete():
    """
    information > delete one dict data by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().dict_delete(params)
    except Exception as e:
        LOG.error("info>dict delete one is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/dict_deletes/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dict_deletes():
    """
    information > delete many dict data by md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().dict_deletes(params)
    except Exception as e:
        LOG.error("info>dict delete many is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/dict_disables/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dict_disables():
    """
    information > batch many dict data status to False by md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().dict_disables(params)
    except Exception as e:
        LOG.error("info>dict status many to false is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/dict_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dict_detail():
    """
    information > get dict detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().dict_detail(params)
    except Exception as e:
        LOG.error("info>dict detail is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/dict_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dict_update():
    """
    information > update dict data information by md5, contain:
        - key
        - value
        - description 描述
        - status 状态
        - order_id 排序ID
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().dict_update(params)
    except Exception as e:
        LOG.error("info>dict update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/dict_names/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dict_names():
    """
    information > get enum names list: key-value
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().dict_names(params)
    except Exception as e:
        LOG.error("info>dict names is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/dict_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dict_add():
    """
    information > add enum model
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().dict_add(params)
    except Exception as e:
        LOG.error("info>dict add is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/api_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def api_add():
    """
    information > add new api model, contain:
        - blueprint
        - apiname
        - type
        - short
        - long
        - order_id
    其中:
        - endpoint = blueprint.apiname
        - path = /blueprint/apiname
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().api_add(params)
    except Exception as e:
        LOG.error("info>api add is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/api_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def api_list():
    """
    information > get api list from api table by params
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().api_list(params)
    except Exception as e:
        LOG.error("info>api list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/api_delete/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def api_delete():
    """
    information > delete one api data by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().api_delete(params)
    except Exception as e:
        LOG.error("info>api delete one is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/api_deletes/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def api_deletes():
    """
    information > delete many api data by md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().api_deletes(params)
    except Exception as e:
        LOG.error("info>api delete many is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/api_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def api_detail():
    """
    information > get api detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().api_detail(params)
    except Exception as e:
        LOG.error("info>api detail is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/api_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def api_update():
    """
    information > api dict data information by md5, contain:
        - blueprint
        - apiname
        - type
        - short
        - long
        - order_id
    其中:
        - endpoint = blueprint.apiname
        - path = /blueprint/apiname
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().api_update(params)
    except Exception as e:
        LOG.error("info>api update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/api_types/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def api_types():
    """
    information > get api type list: key-value
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().api_types(params)
    except Exception as e:
        LOG.error("info>api type is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/depart_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def depart_list():
    """
    information > department list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().depart_list(params)
    except Exception as e:
        LOG.error("info>depart list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/depart_update_tree/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def depart_update_tree():
    """
    information > update department tree information
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().depart_update_tree(params)
    except Exception as e:
        LOG.error("info>depart update tree is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/depart_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def depart_init():
    """
    department init params
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().depart_init(params)
    except Exception as e:
        LOG.error("info>depart init is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@info.route('/depart_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def depart_add():
    """
    add new department to db table department
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return InfoService().depart_add(params)
    except Exception as e:
        LOG.error("info>depart add is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

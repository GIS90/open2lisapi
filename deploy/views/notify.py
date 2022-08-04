# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    message views

base_info:
    __author__ = "PyGo"
    __time__ = "2022/7/12 22:09"
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
# usage: /usr/bin/python message.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS

from deploy.utils.logger import logger as LOG
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import timeer
from deploy.services.notify import NotifyService


notify = Blueprint('notify', __name__, url_prefix='/notify')
CORS(notify, supports_credentials=True)


@notify.route('/dtalk_list/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_list():
    """
    get dtalk message list from db table dtalk_message by parameters
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_list(params)
    except Exception as e:
        LOG.error("notify>dtalk list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_delete/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_delete():
    """
    delete one dtalk data by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_delete(params)
    except Exception as e:
        LOG.error("office>delete one dtalk is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_deletes/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_deletes():
    """
    delete many dtalk data by md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_deletes(params)
    except Exception as e:
        LOG.error("office>delete many dtalk is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_detail/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_detail():
    """
    get dtalk detail information, by file md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_detail(params)
    except Exception as e:
        LOG.error("office>dtalk detail is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_update/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_update():
    """
    update dtalk information, contain:
        - name 文件名称
        - title 消息标题
        - set_sheet 设置的sheet
    by file md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_update(params)
    except Exception as e:
        LOG.error("office>dtalk update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_change_sheet/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_change_sheet():
    """
    dtalk change sheet by sheet index
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_change_sheet(params)
    except Exception as e:
        LOG.error("office>dtalk change sheet is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_list/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_robot_list():
    """
    get dtalk robot list from db table dtalk_robot by parameters
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_robot_list(params)
    except Exception as e:
        LOG.error("notify>dtalk robot list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_add/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_robot_add():
    """
    add new dtalk robot to db table one data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_robot_add(params)
    except Exception as e:
        LOG.error("authority>dtalk robot add is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_delete/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_robot_delete():
    """
    delete one dtalk robot data by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_robot_delete(params)
    except Exception as e:
        LOG.error("office>delete one dtalk robot is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_deletes/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_robot_deletes():
    """
    delete many dtalk robot data by md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_robot_deletes(params)
    except Exception as e:
        LOG.error("office>delete many dtalk robot is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_detail/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_robot_detail():
    """
    get dtalk robot detail information, by file md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_robot_detail(params)
    except Exception as e:
        LOG.error("office>dtalk robot detail is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_update/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_robot_update():
    """
    update dtalk robot information, contain:
        - name 名称
        - key
        - secret
        - description 描述
        - select 选择
    by file md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_robot_update(params)
    except Exception as e:
        LOG.error("office>dtalk robot update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_select/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def dtalk_robot_select():
    """
    set dtalk robot select status, by file md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_robot_select(params)
    except Exception as e:
        LOG.error("office>dtalk robot select is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()



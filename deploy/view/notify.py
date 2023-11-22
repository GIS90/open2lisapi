# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    notify view
    通知模块

content：
    - 钉钉绩效
    - 短信通知
    - 企业微信通知
    详情API请查阅代码，主要包含list、detail、add、update、delete

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
# from deploy.utils.utils import timeer   # change to use watcher
from deploy.utils.watcher import watcher
from deploy.service.notify import NotifyService


notify = Blueprint(name='notify', import_name=__name__, url_prefix='/notify')
CORS(notify, supports_credentials=True)


@notify.route('/dtalk_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
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
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_delete():
    """
    软删除
    delete one dtalk data by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_delete(params)
    except Exception as e:
        LOG.error("notify>delete one dtalk is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_deletes():
    """
    软删除
    delete many dtalk data by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_deletes(params)
    except Exception as e:
        LOG.error("notify>delete many dtalk is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_detail():
    """
    get the latest dtalk message detail information by md5
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
        LOG.error("notify>dtalk detail is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_update():
    """
    update dtalk information by md5, contain:
        - name 文件名称
        - title 消息标题
        - set_sheet 设置的sheet
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
        LOG.error("notify>dtalk update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_change_sheet/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_change_sheet():
    """
    dtalk change sheet by sheet index
    设置中切换sheet展示的内容切换
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
        LOG.error("notify>dtalk change sheet is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
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
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
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
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_robot_delete():
    """
    delete one dtalk robot data by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_robot_delete(params)
    except Exception as e:
        LOG.error("notify>delete one dtalk robot is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_robot_deletes():
    """
    delete many dtalk robot data by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_robot_deletes(params)
    except Exception as e:
        LOG.error("notify>delete many dtalk robot is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_robot_detail():
    """
    get dtalk robot detail information by md5 from dtalk_robot table
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
        LOG.error("notify>dtalk robot detail is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_robot_update():
    """
    update dtalk robot information by md5, contain:
        - name 名称
        - key
        - secret
        - description 描述
        - select 选择
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
        LOG.error("notify>dtalk robot update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_select/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_robot_select():
    """
    set dtalk robot default select status by md5
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
        LOG.error("notify>dtalk robot select is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_robot_ping/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_robot_ping():
    """
    dtalk robot test to ping
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_robot_ping(params)
    except Exception as e:
        LOG.error("notify>dtalk robot ping is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_send_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_send_init():
    """
    dtalk send message initialize data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_send_init(params)
    except Exception as e:
        LOG.error("notify>dtalk send init data is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/dtalk_send/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def dtalk_send():
    """
    dtalk send message to user
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().dtalk_send(params)
    except Exception as e:
        LOG.error("notify>dtalk send is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_robot_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_robot_list():
    """
    get qywx robot list from db table qywx_robot by parameters
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_robot_list(params)
    except Exception as e:
        LOG.error("notify>qywx robot list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_robot_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_robot_add():
    """
    add new qywx robot to db table one data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_robot_add(params)
    except Exception as e:
        LOG.error("authority>qywx robot add is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_robot_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_robot_delete():
    """
    delete one qywx robot data by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_robot_delete(params)
    except Exception as e:
        LOG.error("notify>delete one qywx robot is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_robot_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_robot_deletes():
    """
    delete many qywx robot data by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_robot_deletes(params)
    except Exception as e:
        LOG.error("notify>delete many qywx robot is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_robot_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_robot_detail():
    """
    get qywx robot latest detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_robot_detail(params)
    except Exception as e:
        LOG.error("notify>qywx robot detail is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_robot_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_robot_update():
    """
    update qywx robot information, contain(base information):
        - name 名称
        - key
        - secret
        - description 描述
        - select 选择
    by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_robot_update(params)
    except Exception as e:
        LOG.error("notify>qywx robot update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_robot_select/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_robot_select():
    """
    set qywx robot default select status by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_robot_select(params)
    except Exception as e:
        LOG.error("notify>qywx robot select is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_robot_ping/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_robot_ping():
    """
    qywx robot test to ping
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_robot_ping(params)
    except Exception as e:
        LOG.error("notify>qywx robot ping is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_list():
    """
    get qywx message list from db table qywx_message by parameters
    :return: many json data
    """
    try:
        if request.method == 'GET':
            return Status(
                211, 'failure', StatusMsgs.get(211), {}).json()
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_list(params)
    except Exception as e:
        LOG.error("notify>qywx list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_delete():
    """
    delete one qywx message data by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_delete(params)
    except Exception as e:
        LOG.error("notify>delete one qywx message is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_deletes():
    """
    delete many qywx message data by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_deletes(params)
    except Exception as e:
        LOG.error("notify>delete many qywx message is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_detail():
    """
    get the latest qywx message detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_detail(params)
    except Exception as e:
        LOG.error("notify>qywx detail is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_update():
    """
    update qywx message information, contain:
        - title 消息标题
        - content 消息内容
        - type 消息类型
        - user 用户列表
        - robot 机器人
    by data md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_update(params)
    except Exception as e:
        LOG.error("notify>qywx update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_add():
    """
    add new qywx message data, information content: title, content, type
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_add(params)
    except Exception as e:
        LOG.error("notify>qywx add is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_add_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_add_init():
    """
    新增企业微信消息记录初始化dialog枚举数据
    特殊：get，无参
    :return: many json data
    """
    if request.method == 'POST':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # no parameters
        params = request.args
        return NotifyService().qywx_add_init(params)
    except Exception as e:
        LOG.error("notify>qywx add init is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_send_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_send_init():
    """
    发送企业微信消息记录初始化数据
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_send_init(params)
    except Exception as e:
        LOG.error("notify>qywx send init is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_send/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_send():
    """
    qywx send message to user list
    发送企业微信消息
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_send(params)
    except Exception as e:
        LOG.error("notify>qywx send is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_send_init_temp/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_send_init_temp():
    """
    发送企业微信消息记录初始化数据
    【临时】
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_send_init_temp(params)
    except Exception as e:
        LOG.error("notify>qywx send init temp is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_send_temp/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_send_temp():
    """
    qywx send message to user list
    发送企业微信消息【临时】
    :return: json data

    【废弃，与qywx_send结合】
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_send_temp(params)
    except Exception as e:
        LOG.error("notify>qywx send temp is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_sendback/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_sendback():
    """
    撤销最近24小时内发的企业微信消息
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return NotifyService().qywx_sendback(params)
    except Exception as e:
        LOG.error("notify>qywx sendback is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@notify.route('/qywx_temp_upload/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def qywx_temp_upload():
    """
    企业微信 upload temp file, contain: image图片、voice音频、video视频、file文件
    :return: json data，contain: media_id
    多文件上传，只需要获取第一个
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.form
        # 文件
        files = request.files
        if not files:
            return Status(
                216, 'failure', StatusMsgs.get(216), {}).json()
        for f in files:
            if not f: continue
            upload_file = files.get(f)

        return NotifyService().qywx_temp_upload(params, upload_file)
    except Exception as e:
        LOG.error("notify>qywx temp upload is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()

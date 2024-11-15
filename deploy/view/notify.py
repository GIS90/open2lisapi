# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    notify view
    通知模块
      - 钉钉[dtalk]
      - 企业微信[qywx]

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

from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.decorator import watch_except
from deploy.utils.watcher import watcher
from deploy.service.notify import NotifyService


notify = Blueprint(name='notify', import_name=__name__, url_prefix='/notify')
CORS(notify, supports_credentials=True)

notify_service = NotifyService()


@notify.route('/dtalk_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_list():
    """
    get dtalk message list from db table dtalk_message by parameters
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_list(params)


@notify.route('/dtalk_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_delete():
    """
    软删除
    delete one dtalk data by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_delete(params)


@notify.route('/dtalk_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_deletes():
    """
    软删除
    delete many dtalk data by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_deletes(params)


@notify.route('/dtalk_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_detail():
    """
    get the latest dtalk message detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_detail(params)


@notify.route('/dtalk_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
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
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_update(params)


@notify.route('/dtalk_change_sheet/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_change_sheet():
    """
    dtalk change sheet by sheet index
    设置中切换sheet展示的内容切换
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_change_sheet(params)


@notify.route('/dtalk_robot_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_robot_list():
    """
    get dtalk robot list from db table dtalk_robot by parameters
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_robot_list(params)


@notify.route('/dtalk_robot_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_robot_add():
    """
    add new dtalk robot to db table one data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_robot_add(params)


@notify.route('/dtalk_robot_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_robot_delete():
    """
    delete one dtalk robot data by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_robot_delete(params)


@notify.route('/dtalk_robot_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_robot_deletes():
    """
    delete many dtalk robot data by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_robot_deletes(params)


@notify.route('/dtalk_robot_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_robot_detail():
    """
    get dtalk robot detail information by md5 from dtalk_robot table
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_robot_detail(params)


@notify.route('/dtalk_robot_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
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
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_robot_update(params)


@notify.route('/dtalk_robot_select/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_robot_select():
    """
    set dtalk robot default select status by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_robot_select(params)


@notify.route('/dtalk_robot_ping/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_robot_ping():
    """
    dtalk robot test to ping
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_robot_ping(params)


@notify.route('/dtalk_send_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_send_init():
    """
    dtalk send message initialize data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_send_init(params)


@notify.route('/dtalk_send/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dtalk_send():
    """
    dtalk send message to user
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.dtalk_send(params)


@notify.route('/qywx_robot_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_robot_list():
    """
    get qywx robot list from db table qywx_robot by parameters
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_robot_list(params)


@notify.route('/qywx_robot_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_robot_add():
    """
    add new qywx robot to db table one data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_robot_add(params)


@notify.route('/qywx_robot_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_robot_delete():
    """
    delete one qywx robot data by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_robot_delete(params)


@notify.route('/qywx_robot_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_robot_deletes():
    """
    delete many qywx robot data by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_robot_deletes(params)


@notify.route('/qywx_robot_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_robot_detail():
    """
    get qywx robot latest detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_robot_detail(params)


@notify.route('/qywx_robot_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
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
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_robot_update(params)


@notify.route('/qywx_robot_select/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_robot_select():
    """
    set qywx robot default select status by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_robot_select(params)


@notify.route('/qywx_robot_ping/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_robot_ping():
    """
    qywx robot test to ping
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_robot_ping(params)


@notify.route('/qywx_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_list():
    """
    get qywx message list from db table qywx_message by parameters
    :return: many json data
    """

    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_list(params)


@notify.route('/qywx_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_delete():
    """
    delete one qywx message data by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_delete(params)


@notify.route('/qywx_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_deletes():
    """
    delete many qywx message data by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_deletes(params)


@notify.route('/qywx_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_detail():
    """
    get the latest qywx message detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_detail(params)


@notify.route('/qywx_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
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
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_update(params)


@notify.route('/qywx_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_add():
    """
    add new qywx message data, information content: title, content, type
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_add(params)


@notify.route('/qywx_add_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_add_init():
    """
    新增企业微信消息记录初始化dialog枚举数据
    特殊：get，无参
    :return: many json data
    """
    if request.method == 'POST':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # GET请求参数
    params = request.args
    return notify_service.qywx_add_init(params)


@notify.route('/qywx_send_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_send_init():
    """
    发送企业微信消息记录初始化数据
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_send_init(params)


@notify.route('/qywx_send/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
# @watch_except
def qywx_send():
    """
    qywx send message to user list
    发送企业微信消息
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_send(params)


@notify.route('/qywx_send_init_temp/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_send_init_temp():
    """
    发送企业微信消息记录初始化数据
    【临时】
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_send_init_temp(params)


@notify.route('/qywx_send_temp/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_send_temp():
    """
    qywx send message to user list
    发送企业微信消息【临时】
    :return: json data

    【废弃，与qywx_send结合】
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_send_temp(params)


@notify.route('/qywx_sendback/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_sendback():
    """
    撤销最近24小时内发的企业微信消息
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.qywx_sendback(params)


@notify.route('/qywx_temp_upload/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def qywx_temp_upload():
    """
    企业微信 upload temp file, contain: image图片、voice音频、video视频、file文件
    :return: json data，contain: media_id
    多文件上传，只需要获取第一个
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.form
    # 文件
    files = request.files
    if not files:
        return Status(
            450, StatusEnum.FAILURE.value, StatusMsgs.get(450), {}).json()
    for f in files:
        if not f: continue
        upload_file = files.get(f)

    return notify_service.qywx_temp_upload(params, upload_file)


@notify.route('/sms_add_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sms_add_init():
    """
    新增短信消息记录初始化dialog枚举数据
    特殊：get，无参
    :return: many json data
    """
    if request.method == 'POST':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # GET请求参数
    params = request.args
    return notify_service.sms_add_init(params)


@notify.route('/sms_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
# @watch_except
def sms_add():
    """
    add new message message data
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.sms_add(params)


@notify.route('/sms_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sms_list():
    """
    get many sms data list
    :return: many json data
    """

    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.sms_list(params)


@notify.route('/sms_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sms_delete():
    """
    delete one sms data by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.sms_delete(params)


@notify.route('/sms_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sms_deletes():
    """
    delete many sms data by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.sms_deletes(params)


@notify.route('/sms_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sms_detail():
    """
    get the latest sms detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.sms_detail(params)


@notify.route('/sms_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sms_update():
    """
    update sms information, by data md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return notify_service.sms_update(params)


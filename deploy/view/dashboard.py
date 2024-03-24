# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    bashboard view
    - 图表[chart]
    - 功能快捷键[shortcut]

base_info:
    __author__ = "PyGo"
    __time__ = "2022/8/19 15:18"
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
# usage: /usr/bin/python dashboard.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.decorator import watch_except
from deploy.utils.watcher import watcher
from deploy.service.dashboard import DashboardService


dashboard = Blueprint(name='dashboard', import_name=__name__, url_prefix='/dashboard')
CORS(dashboard, supports_credentials=True)

dashboard_service = DashboardService()


@dashboard.route('/pan/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def pan():
    """
    dashboard pan chart data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return dashboard_service.pan(params)


@dashboard.route('/pan_chart/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def pan_chart():
    """
    dashboard pan chart data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return dashboard_service.pan_chart(params)


@dashboard.route('/index/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def index():
    """
    dashboard index chart data initialize
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return dashboard_service.index(params)


@dashboard.route('/shortcut/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def shortcut():
    """
    dashboard short cut data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return dashboard_service.shortcut(params)


@dashboard.route('/shortcut_edit/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def shortcut_edit():
    """
    dashboard short cut edit data list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return dashboard_service.shortcut_edit(params)


@dashboard.route('/shortcut_save/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def shortcut_save():
    """
    dashboard short cut edit data save
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return dashboard_service.shortcut_save(params)


# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    bashboard apis
    - pan: 初始化Dashboard Pan

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
from datetime import datetime
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from deploy.utils.logger import logger as LOG
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import timeer
from deploy.utils.watcher import watcher
from deploy.services.dashboard import DashboardService
from deploy.services.request import RequestService


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')
CORS(dashboard, supports_credentials=True)


@dashboard.route('/pan/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def pan():
    """
    dashboard pan chart data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        res = DashboardService().pan(params)
        return res
    except Exception as e:
        LOG.error("dashboard>pan is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@dashboard.route('/pan_chart/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def pan_chart():
    """
    dashboard pan chart data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        res = DashboardService().pan_chart(params)
        return res
    except Exception as e:
        LOG.error("dashboard>pan chart is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@dashboard.route('/index/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def index():
    """
    dashboard index chart data initialize
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    # 参数
    params = request.get_json() or {}
    res = DashboardService().index(params)
    try:
        return res
    except Exception as e:
        LOG.error("dashboard>index is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@dashboard.route('/shortcut/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def shortcut():
    """
    dashboard short cut data
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return DashboardService().shortcut(params)
    except Exception as e:
        LOG.error("dashboard>shortcut is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@dashboard.route('/shortcut_edit/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def shortcut_edit():
    """
    dashboard short cut edit data list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return DashboardService().shortcut_edit(params)
    except Exception as e:
        LOG.error("dashboard>shortcut edit is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@dashboard.route('/shortcut_save/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def shortcut_save():
    """
    dashboard short cut edit data save
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return DashboardService().shortcut_save(params)
    except Exception as e:
        LOG.error("dashboard>shortcut save is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

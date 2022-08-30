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
        LOG.error("info>dict status is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()



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
from deploy.services.sysuser import SysUserService
from deploy.services.request import RequestService
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import timeer


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
        # return OfficeService().excel_source_list(params)
    except Exception as e:
        LOG.error("notify>dtalk message list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

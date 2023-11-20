# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2023/9/7 20:59"
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
# usage: /usr/bin/python apis.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS

from deploy.service.api import ApiService
from deploy.utils.logger import logger as LOG
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.watcher import watcher


api = Blueprint(name='api', import_name=__name__, url_prefix='/api')
CORS(api, supports_credentials=True)


@api.route('/demo/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def demo():
    """
    api: demo
    :return: json data
    """
    if request.method == 'POST':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return ApiService().demo(params)
    except Exception as e:
        LOG.error("api>demo is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

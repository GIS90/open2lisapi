# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    api view

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
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.watcher import watcher
from deploy.utils.decorator import watch_except


api = Blueprint(name='api', import_name=__name__, url_prefix='/api')
CORS(api, supports_credentials=True)

api_service = ApiService()


@api.route('/demo/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def api_demo():
    """
    api: demo
    :return: json data
    """
    if request.method == 'POST':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # JSON请求参数
    params = request.get_json() or {}
    return api_service.api_demo(params)


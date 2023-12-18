# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    watcher
    用于API计时打点，写入request表

base_info:
    __author__ = "PyGo"
    __time__ = "2022/8/26 23:02"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    from flask import request
    @watcher(watcher_args=request)
    watcher_args参数为request对象，里面包含blueprint, endpoint, method, path, header等请求参数

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python watcher.py
# ------------------------------------------------------------
from datetime import datetime
from functools import wraps
from pprint import pprint

from deploy.utils.logger import logger as LOG
from deploy.utils.utils import get_rtx_id
from deploy.service.request import RequestService


# 声明一个全局RequestService对象
request_service = RequestService()


REQUEST_METHODS = ['GET', 'POST', 'DELETE', 'PUT']
GLOBAL_NEW_REQUEST_ENDPOINT = [
    'dashboard.pan',
    'dashboard.shortcut',
    'dashboard.pan_chart',
    'dashboard.index',
    'auth.user_list',
    'info.dict_list',
    'search.sqlbase_list',
    'info.depart_detail',
    'image.profile_avatar_list',
    'common.file_uploads',
]


# method desc: API request to write database table [request]
def __add_request(request, cost, rtx=None):
    """
    API request information to insert into request table
    :param request: API request object parameters
    :param cost: API run time, unit is second
    :param rtx: request user rtx-id
        - 1.request get "X-Rtx-Id"
        - 2.no request by manual set
    """
    rtx_id = get_rtx_id(request) or rtx    # not rtx_id, no insert
    if not rtx_id:
        return False
    method = getattr(request, 'method')     # method allow only get or post
    if method and str(method).upper() not in REQUEST_METHODS:
        return False
    if hasattr(request, 'endpoint') and getattr(request, 'endpoint') in GLOBAL_NEW_REQUEST_ENDPOINT:
        RequestService().add_request(request=request, cost=cost, rtx=rtx_id)
    else:
        request_service.add_request(request=request, cost=cost, rtx=rtx_id)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>> API打点计时器 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def watcher(watcher_args):
    def _watcher(fn):
        @wraps(fn)
        def _wrapper(*args, **kwargs):
            start = datetime.now()
            res = fn(*args, **kwargs)
            end = datetime.now()
            cost = round((end-start).microseconds * pow(0.1, 6), 3)   # API run time, unit is second
            if watcher_args:
                __add_request(request=watcher_args, cost=cost)  # API request to write database table [request]
            LOG.info('@Watcher [%s] is run: %s' % (getattr(watcher_args, 'endpoint') or fn.__name__, cost))
            return res

        return _wrapper
    return _watcher

# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    authority views

base_info:
    __author__ = "PyGo"
    __time__ = "2022/5/9 22:47"
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
# usage: /usr/bin/python authority.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from deploy.utils.logger import logger as LOG
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import timeer
from deploy.services.authority import AuthorityService


auth = Blueprint('auth', __name__, url_prefix='/auth')
CORS(auth, supports_credentials=True)


@auth.route('/role/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def role_list():
    """
    get role list from db table role
    many list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return AuthorityService().role_list(params)
    except Exception as e:
        LOG.error("excel>list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    convert api views

base_info:
    __author__ = "PyGo"
    __time__ = "2022/6/8 20:05"
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
# usage: /usr/bin/python convert.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from deploy.utils.logger import logger as LOG
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import timeer


convert = Blueprint('convert', __name__, url_prefix='/convert')
CORS(convert, supports_credentials=True)


@convert.route('/pdf2word/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def pdf2word_list():
    """
    get pdf2word list from db table by parameters
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        # return AuthorityService().role_list(params)
    except Exception as e:
        LOG.error("pdf2word>pdf2word list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

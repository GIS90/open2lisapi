# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    excel views

base_info:
    __author__ = "PyGo"
    __time__ = "2022/3/29 11:02 下午"
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
# usage: /usr/bin/python excel.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from deploy.utils.logger import logger as LOG
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import timeer


excel = Blueprint('excel', __name__, url_prefix='/excel')
CORS(excel, supports_credentials=True)


@excel.route('/upload/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def upload():
    """
    excel file upload to server
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()
    try:
        # 参数
        form = request.form
        rtx_id = form.get('rtx_id')
        # 文件
        files = request.files

        if not files or (files and not files.get('files')):
            return Status(
                216, 'failure', StatusMsgs.get(216), {}
            ).json()

        # return SysUserService().update_avatar_by_rtx(rtx_id, files.get('avatar'))
    except Exception as e:
        LOG.error("user>avatar is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


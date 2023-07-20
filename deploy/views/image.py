# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2023/7/20 23:21"
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
# usage: /usr/bin/python image.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from deploy.utils.logger import logger as LOG
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.watcher import watcher
from deploy.services.image import ImageService


image = Blueprint('image', __name__, url_prefix='/image')
CORS(image, supports_credentials=True)


@image.route('/avatar_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def avatar_list():
    """
    image > avatar list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()
    try:
        # 参数
        params = request.get_json() or {}
        return ImageService().avatar_list(params)
    except Exception as e:
        LOG.error("image>avatar list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

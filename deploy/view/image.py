# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    image view
      - 用户头像[avatar]

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

from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.watcher import watcher
from deploy.service.image import ImageService
from deploy.utils.decorator import watch_except


image = Blueprint(name='image', import_name=__name__, url_prefix='/image')
CORS(image, supports_credentials=True)

image_service = ImageService()


@image.route('/profile_avatar_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def profile_avatar_list():
    """
    image > profile avatar list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return image_service.profile_avatar_list(params)


@image.route('/profile_avatar_set/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def profile_avatar_set():
    """
    image > profile avatar set
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return image_service.profile_avatar_set(params)

# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    common apis
    通用API模块
    - upload 上传单文件
    - upload 多文件上传

base_info:
    __author__ = "PyGo"
    __time__ = "2022/6/10 22:41"
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
# usage: /usr/bin/python common.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from deploy.utils.logger import logger as LOG
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
# from deploy.utils.utils import timeer   # change to use watcher
from deploy.utils.watcher import watcher
from deploy.service.common import CommonService


common = Blueprint(name='common', import_name=__name__, url_prefix='/common')
CORS(common, supports_credentials=True)


@common.route('/file_upload/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def file_upload():
    """
    one file upload to server(file store object)
    :return: json data

    前端form表单上传文件input name：files
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.form
        # 文件
        files = request.files
        if not files or (files and not files.get('files')):
            return Status(
                216, 'failure', StatusMsgs.get(216), {}).json()

        return CommonService().file_upload(params, request.files.get('files'))
    except Exception as e:
        LOG.error("common>file upload is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@common.route('/file_uploads/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def file_uploads():
    """
    many file upload to server(file store object)
    :return: json data

    前端form表单上传文件input name：files
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.form
        # 文件
        files = request.files
        if not files:
            return Status(
                216, 'failure', StatusMsgs.get(216), {}).json()

        return CommonService().file_uploads(params, files)
    except Exception as e:
        LOG.error("common>file uploads is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@common.route('/image_wangeditor/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def image_wangeditor():
    """
    one image wang editor upload to server(file store object)
    :return: json data

    前端form表单上传文件input name：files
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.form
        # 文件
        files = request.files
        if not files or (files and not files.get('files')):
            return Status(
                216, 'failure', StatusMsgs.get(216), {}).json()

        return CommonService().image_wangeditor(params, request.files.get('files'))
    except Exception as e:
        LOG.error("common>image wang editor upload is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

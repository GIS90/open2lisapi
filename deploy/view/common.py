# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    common view
    通用API模块
        - 上传单文件[file_upload]
        - 多文件上传[file_uploads]
        - 富文本编辑器图片上传[image_wangeditor]

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

from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.watcher import watcher
from deploy.utils.decorator import watch_except
from deploy.service.common import CommonService


common = Blueprint(name='common', import_name=__name__, url_prefix='/common')
CORS(common, supports_credentials=True)

common_service = CommonService()


@common.route('/file_upload/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def file_upload():
    """
    one file upload to server(file store object)
    :return: json data

    前端form表单单文件上传
    input name：files
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # FORM表单参数
    params = request.form
    # 文件
    files = request.files
    if not files or (files and not files.get('files')):
        return Status(
            450, StatusEnum.FAILURE.value, StatusMsgs.get(450), {}).json()

    return common_service.file_upload(params, request.files.get('files'))


@common.route('/file_uploads/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def file_uploads():
    """
    many file upload to server(file store object)
    :return: json data

    前端form表单多文件上传
    input name：files
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # FORM表单参数
    params = request.form
    # 文件
    files = request.files
    if not files:
        return Status(
            450, StatusEnum.FAILURE.value, StatusMsgs.get(450), {}).json()

    return common_service.file_uploads(params, files)


@common.route('/image_wangeditor/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def image_wangeditor():
    """
    one image wang editor upload to server(file store object)
    :return: json data

    富文本编辑器图片上传[单]
    input name：files
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # FORM表单参数
    params = request.form
    # 文件
    files = request.files
    if not files or (files and not files.get('files')):
        return Status(
            450, StatusEnum.FAILURE.value, StatusMsgs.get(450), {}).json()

    return common_service.image_wangeditor(params, request.files.get('files'))


@common.route('/download_excel_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def download_excel_init():
    """
    Excel data download initialize parameter
    """
    if request.method == 'POST':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.args or {}
    return common_service.download_excel_init(params)


@common.route('/download_excel/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def download_excel():
    """
    Excel data download initialize parameter
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return common_service.download_excel(params)


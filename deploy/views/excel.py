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
from deploy.services.excel import ExcelService


excel = Blueprint('excel', __name__, url_prefix='/excel')
CORS(excel, supports_credentials=True)


@excel.route('/list/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def list():
    """
    get excel list from db
    many file
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().excel_list(params)
    except Exception as e:
        LOG.error("excel>list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/upload/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def upload():
    """
    excel file upload to server
    one file
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()
    try:
        # 参数
        params = request.form
        # 文件
        files = request.files
        if not files or (files and not files.get('files')):
            return Status(
                216, 'failure', StatusMsgs.get(216), {}
            ).json()

        return ExcelService().excel_upload(params, request.files.get('files'))
    except Exception as e:
        LOG.error("excel>upload is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/uploads/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def uploads():
    """
    excel file upload to server
    many file
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.form
        # 文件
        files = request.files
        if not files:
            return Status(
                216, 'failure', StatusMsgs.get(216), {}
            ).json()

        return ExcelService().excel_upload_m(params, files)
    except Exception as e:
        LOG.error("excel>uploads is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/update/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def update():
    """
    update excel file information
    by excel file md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().excel_update(params)
    except Exception as e:
        LOG.error("excel>update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/delete/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def delete():
    """
    delete one excel file by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().excel_delete(params)
    except Exception as e:
        LOG.error("excel>delete is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/deletes/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def deletes():
    """
    delete many excel file by md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().excel_deletes(params)
    except Exception as e:
        LOG.error("excel>deletes is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/merge/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def merge():
    """
    many excel file to merge by file md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().excel_merge(params)
    except Exception as e:
        LOG.error("excel>merge is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

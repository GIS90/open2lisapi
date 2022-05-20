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
def source_list():
    """
    get excel list from db table excel_source
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().excel_source_list(params)
    except Exception as e:
        LOG.error("excel>source list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/upload/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def upload():
    """
    one excel file upload to server(file store object)
    :return: json data
    单文件上传
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
    one excel file upload to server(file store object)
    :return: json data
    多文件上传
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


@excel.route('/updates/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def update_source():
    """
    update source file information, contain:
        - name 文件名称
        - set_sheet 设置的Sheet
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
        return ExcelService().update_source(params)
    except Exception as e:
        LOG.error("excel>update source excel file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/delete/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def source_delete():
    """
    delete one source excel file by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().source_delete(params)
    except Exception as e:
        LOG.error("excel>delete one source file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/deletes/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def source_deletes():
    """
    delete many source excel file by md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().source_deletes(params)
    except Exception as e:
        LOG.error("excel>delete many source file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/merge/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def merge():
    """
    many excel file to merge one excel file,
    many file list by file md5 list
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


@excel.route('/history/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def history_list():
    """
    get history excel list from db table excel_result
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
        return ExcelService().excel_history_list(params)
    except Exception as e:
        LOG.error("excel>history list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/updater/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def update_result():
    """
    update result excel file, only update file name
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
        return ExcelService().update_result(params)
    except Exception as e:
        LOG.error("excel>update result excel file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/deleter/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def result_delete():
    """
    delete one result excel file by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().result_delete(params)
    except Exception as e:
        LOG.error("excel>delete result file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/deletesr/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def result_deletes():
    """
    delete many result excel file by md5 list
    parameter list is List type
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().result_deletes(params)
    except Exception as e:
        LOG.error("excel>batch deletes result file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/initsplit/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def init_split_params():
    """
    initialize the result excel file split parameter
    :return: json data, contain:
        sheet_index, sheet_names, column_names, excel_split_store, split_type, bool_type
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().init_split_params(params)
    except Exception as e:
        LOG.error("excel>initialize split parameter is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/sheetheader/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def get_sheet_header():
    """
    get sheet headers by sheet index
    excel_source table
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().get_sheet_header(params)
    except Exception as e:
        LOG.error("excel>get sheet headers is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@excel.route('/split/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def split():
    """
    split method, split parameters is many
    function: one file to split many file
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}
        ).json()

    try:
        # 参数
        params = request.get_json() or {}
        return ExcelService().excel_split(params)
    except Exception as e:
        LOG.error("excel>split is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

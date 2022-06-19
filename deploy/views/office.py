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
from deploy.services.office import OfficeService


office = Blueprint('office', __name__, url_prefix='/office')
CORS(office, supports_credentials=True)


@office.route('/upload/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def upload():
    """
    one office file upload to server(file store object)
    :return: json data
    单文件上传
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

        return OfficeService().office_upload(params, request.files.get('files'))
    except Exception as e:
        LOG.error("office>upload is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/uploads/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def uploads():
    """
    many office file upload to server(file store object)
    :return: json data
    多文件上传
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

        return OfficeService().office_upload_m(params, files)
    except Exception as e:
        LOG.error("office>uploads is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/excel_source_list/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def excel_source_list():
    """
    get excel source list from db table excel_source by parameters
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().excel_source_list(params)
    except Exception as e:
        LOG.error("office>excel source list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/excel_source_update/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def excel_source_update():
    """
    update excel source file information, contain:
        - name 文件名称
        - set_sheet 设置的Sheet
    by excel file md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().excel_source_update(params)
    except Exception as e:
        LOG.error("office>update excel source file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/excel_source_delete/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def excel_source_delete():
    """
    delete one excel source excel file by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().excel_source_delete(params)
    except Exception as e:
        LOG.error("office>delete one excel source file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/excel_source_deletes/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def excel_source_deletes():
    """
    delete many excel source excel file by md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().excel_source_deletes(params)
    except Exception as e:
        LOG.error("office>delete many excel source file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/excel_merge/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def excel_merge():
    """
    many excel file to merge one excel file,
    many file list by file md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().excel_merge(params)
    except Exception as e:
        LOG.error("office>excel merge is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/excel_history_list/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def excel_history_list():
    """
    get excel history excel list from db table excel_result
    many file
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().excel_history_list(params)
    except Exception as e:
        LOG.error("office>excel history list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/excel_result_update/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def excel_result_update():
    """
    update excel result excel file, only update file name
    by excel file md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().excel_result_update(params)
    except Exception as e:
        LOG.error("office>update result excel file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/excel_result_delete/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def excel_result_delete():
    """
    delete one excel result excel file by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().excel_result_delete(params)
    except Exception as e:
        LOG.error("office>delete excel result file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/excel_result_deletes/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def excel_result_deletes():
    """
    delete many excel result excel file by md5 list
    parameter list is List type
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().excel_result_deletes(params)
    except Exception as e:
        LOG.error("office>batch deletes excel result file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/excel_init_split/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def excel_init_split_params():
    """
    initialize the excel result excel file split parameter
    :return: json data, contain:
        sheet_index, sheet_names, column_names, excel_split_store, split_type, bool_type
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().excel_init_split_params(params)
    except Exception as e:
        LOG.error("office>initialize excel split parameter is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/excel_sheet_header/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def excel_sheet_header():
    """
    get sheet headers by sheet index
    excel_source table
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().excel_sheet_header(params)
    except Exception as e:
        LOG.error("office>get excel sheet headers is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/excel_split/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def excel_split():
    """
    split method, split parameters is many
    function: one file to split many file
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().excel_split(params)
    except Exception as e:
        LOG.error("office>split is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/pdf2word_list/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def pdf2word_list():
    """
    get pdf2word list from db table by parameters
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().pdf2word_list(params)
    except Exception as e:
        LOG.error("office>pdf2word list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/office_pdf_update/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def office_pdf_update():
    """
    update office pdf file information, contain:
        - name 文件名称
        - start 转换开始页
        - end 转换结束页
        - pages 指定转换页列表
    by file md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().office_pdf_update(params)
    except Exception as e:
        LOG.error("office>update office pdf file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/office_pdf_delete/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def office_pdf_delete():
    """
    delete one office pdf file by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().office_pdf_delete(params)
    except Exception as e:
        LOG.error("office>delete one office pdf file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@office.route('/office_pdf_deletes/', methods=['GET', 'POST'], strict_slashes=False)
@timeer
def office_pdf_deletes():
    """
    delete many office pdf file by md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return OfficeService().office_pdf_deletes(params)
    except Exception as e:
        LOG.error("office>delete many office pdf file is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()

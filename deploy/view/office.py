# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    office view
      - excel
      - pdf

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

from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.decorator import watch_except
from deploy.utils.watcher import watcher
from deploy.service.office import OfficeService


office = Blueprint(name='office', import_name=__name__, url_prefix='/office')
CORS(office, supports_credentials=True)

office_service = OfficeService()


@office.route('/excel_source_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def excel_source_list():
    """
    get excel source list from db table excel_source by parameters
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.excel_source_list(params)


@office.route('/excel_source_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
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
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.excel_source_update(params)


@office.route('/excel_source_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def excel_source_delete():
    """
    delete one excel source excel file by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.excel_source_delete(params)


@office.route('/excel_source_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def excel_source_deletes():
    """
    delete many excel source excel file by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.excel_source_deletes(params)


@office.route('/excel_merge/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def excel_merge():
    """
    operation method, many excel file to merge one excel file,
    many file list by file md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.excel_merge(params)


@office.route('/excel_history_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def excel_history_list():
    """
    get excel history excel list from db table excel_result
    many file
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.excel_history_list(params)


@office.route('/excel_result_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def excel_result_update():
    """
    update excel result excel file, only update file name
    by excel file md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.excel_result_update(params)


@office.route('/excel_result_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def excel_result_delete():
    """
    delete one excel result excel file by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.excel_result_delete(params)


@office.route('/excel_result_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def excel_result_deletes():
    """
    delete many excel result excel file by md5 list
    parameter list is List type
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.excel_result_deletes(params)


@office.route('/excel_init_split/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def excel_init_split_params():
    """
    initialize the excel result excel file split parameter
    :return: json data, contain:
        sheet_index, sheet_names, column_names, excel_split_store, split_type, bool_type
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.excel_init_split_params(params)


@office.route('/excel_sheet_header/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def excel_sheet_header():
    """
    get sheet headers by sheet index from excel_source table
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.excel_sheet_header(params)


@office.route('/excel_split/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def excel_split():
    """
    split method, split parameters is many
    function: one file to split many file
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.excel_split(params)


@office.route('/pdf2word_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def pdf2word_list():
    """
    get pdf2word list from db table by parameters
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.pdf2word_list(params)


@office.route('/office_pdf_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def office_pdf_detail():
    """
    get office pdf file detail information by file md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.office_pdf_detail(params)


@office.route('/office_pdf_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
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
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.office_pdf_update(params)


@office.route('/office_pdf_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def office_pdf_delete():
    """
    delete one office pdf file by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.office_pdf_delete(params)


@office.route('/office_pdf_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def office_pdf_deletes():
    """
    delete many office pdf file by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.office_pdf_deletes(params)


@office.route('/office_pdf_to/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def office_pdf_to():
    """
    office pdf file convert to word file, one file to convert:
        1.check current file set data
        2.convert pdf file to word
        3.convert success to store object
        4.update transfer information
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.VALUE, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return office_service.office_pdf_to(params)


# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    search view
      - SQL仓库[sqlbase]
      - 知识分享[share]
      - 羊毛工具[sheep]

base_info:
    __author__ = "PyGo"
    __time__ = "2022/12/21 18:22"
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
# usage: /usr/bin/python search.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from deploy.utils.logger import logger as LOG
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.watcher import watcher
from deploy.service.search import SearchService
from deploy.utils.decorator import watch_except


search = Blueprint(name='search', import_name=__name__, url_prefix='/search')
CORS(search, supports_credentials=True)

search_service = SearchService()


@search.route('/sqlbase_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sqlbase_list():
    """
    get sqlbase list from db table sqlbase by parameters
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return search_service.sqlbase_list(params)


@search.route('/sqlbase_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sqlbase_add():
    """
    add new data to db table sqlbase, new data is dict object
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return search_service.sqlbase_add(params)


@search.route('/sqlbase_add_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sqlbase_add_init():
    """
    sqlbase add data initialize enum list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return search_service.sqlbase_add_init(params)


@search.route('/sqlbase_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sqlbase_delete():
    """
    delete one sqlbase data by md5 from sqlbase table
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return search_service.sqlbase_delete(params)


@search.route('/sqlbase_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sqlbase_deletes():
    """
    delete many sqlbase data by md5 list from sqlbase table
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return search_service.sqlbase_deletes(params)


@search.route('/sqlbase_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sqlbase_detail():
    """
    get the latest sqlbase detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return search_service.sqlbase_detail(params)


@search.route('/sqlbase_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def sqlbase_update():
    """
    update sqlbase message information by data md5, contain:
        - title 标题
        - html/text 内容
        - author 作者
        - public—time 发布时间
        - recommend 推荐度
        - database 数据库
        - summary 简述
        - label 标签

    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return search_service.sqlbase_update(params)


@search.route('/share_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def share_list():
    """
    get share data list from db table share by parameters
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return search_service.share_list(params)


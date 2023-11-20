# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    search view

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
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.watcher import watcher
from deploy.service.search import SearchService


search = Blueprint(name='search', import_name=__name__, url_prefix='/search')
CORS(search, supports_credentials=True)


@search.route('/sqlbase_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def sqlbase_list():
    """
    get sqlbase list from db table sqlbase by parameters
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return SearchService().sqlbase_list(params)
    except Exception as e:
        LOG.error("search>sqlbase list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@search.route('/sqlbase_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def sqlbase_add():
    """
    add new data to db table sqlbase, new data is dict object
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return SearchService().sqlbase_add(params)
    except Exception as e:
        LOG.error("search>sqlbase add is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@search.route('/sqlbase_add_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def sqlbase_add_init():
    """
    sqlbase add data initialize enum list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return SearchService().sqlbase_add_init(params)
    except Exception as e:
        LOG.error("search>sqlbase add init is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


@search.route('/sqlbase_delete/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def sqlbase_delete():
    """
    delete one sqlbase data by md5 from sqlbase table
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return SearchService().sqlbase_delete(params)
    except Exception as e:
        LOG.error("search>delete one sqlbase is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@search.route('/sqlbase_deletes/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def sqlbase_deletes():
    """
    delete many sqlbase data by md5 list from sqlbase table
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return SearchService().sqlbase_deletes(params)
    except Exception as e:
        LOG.error("search>delete many sqlbase is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@search.route('/sqlbase_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def sqlbase_detail():
    """
    get the latest sqlbase detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return SearchService().sqlbase_detail(params)
    except Exception as e:
        LOG.error("search>sqlbase detail is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@search.route('/sqlbase_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
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
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return SearchService().sqlbase_update(params)
    except Exception as e:
        LOG.error("search>sqlbase update is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or '服务端API请求发生故障，请稍后尝试', {}).json()


@search.route('/share_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
def share_list():
    """
    get share data list from db table share by parameters
    :return: many json data
    """
    if request.method == 'GET':
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()

    try:
        # 参数
        params = request.get_json() or {}
        return SearchService().share_list(params)
    except Exception as e:
        LOG.error("search>share list is error: %s" % e)
        return Status(501, 'failure',
                      StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试', {}).json()


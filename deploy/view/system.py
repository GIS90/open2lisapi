# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    information view
      - 数据字典[dict]
      - API[api]
      - 树[depart]

base_info:
    __author__ = "PyGo"
    __time__ = "2022/8/30 21:25"
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


ADMIN_AUTH_LIST.extend([ADMIN, model.rtx_id])  # 特权账号 + 数据账号
权限管理，无特权账号
------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python info.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.watcher import watcher
from deploy.service.info import InfoService
from deploy.utils.decorator import watch_except


system = Blueprint(name='system', import_name=__name__, url_prefix='/system')
CORS(system, supports_credentials=True)

info_service = InfoService()


@system.route('/dict_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dict_list():
    """
    system > dict list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.dict_list(params)


@system.route('/dict_status/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dict_status():
    """
    system > change dict data status by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.dict_status(params)


@system.route('/dict_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dict_delete():
    """
    system > delete one dict data by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.dict_delete(params)


@system.route('/dict_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dict_deletes():
    """
    system > delete many dict data by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.dict_deletes(params)


@system.route('/dict_disables/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dict_disables():
    """
    system > batch many dict data status to False by md5 list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.dict_disables(params)


@system.route('/dict_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dict_detail():
    """
    system > get dict detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.dict_detail(params)


@system.route('/dict_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dict_update():
    """
    system > update dict data information by md5, contain:
        - key
        - value
        - description 描述
        - status 状态
        - order_id 排序ID
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.dict_update(params)


@system.route('/dict_names/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dict_names():
    """
    system > get enum names list: key-value
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.dict_names(params)


@system.route('/dict_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def dict_add():
    """
    system > add enum model
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.dict_add(params)


@system.route('/api_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def api_add():
    """
    system > add new api model, contain:
        - blueprint
        - apiname
        - type
        - short
        - long
        - order_id
    其中:
        - endpoint = blueprint.apiname
        - path = /blueprint/apiname
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.api_add(params)


@system.route('/api_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def api_list():
    """
    system > get api list from api table by params
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.api_list(params)


@system.route('/api_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def api_delete():
    """
    system > delete one api data by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.api_delete(params)


@system.route('/api_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def api_deletes():
    """
    system > delete many api data by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.api_deletes(params)


@system.route('/api_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def api_detail():
    """
    system > get api detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.api_detail(params)


@system.route('/api_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def api_update():
    """
    system > api dict data information by md5, contain:
        - blueprint
        - apiname
        - type
        - short
        - long
        - order_id
    其中:
        - endpoint = blueprint.apiname
        - path = /blueprint/apiname
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.api_update(params)


@system.route('/api_types/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def api_types():
    """
    system > get api type list: key-value
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.api_types(params)


@system.route('/depart_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def depart_list():
    """
    system > department list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.depart_list(params)


@system.route('/depart_update_tree/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def depart_update_tree():
    """
    system > update department tree information
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.depart_update_tree(params)


@system.route('/depart_init/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def depart_init():
    """
    department init params
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.depart_init(params)


@system.route('/depart_add/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def depart_add():
    """
    add new department to db table department
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.depart_add(params)


@system.route('/depart_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def depart_delete():
    """
    delete department by node md5-id
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.depart_delete(params)


@system.route('/depart_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def depart_detail():
    """
    department detail informations by node md5-id
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.depart_detail(params)


@system.route('/depart_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def depart_update():
    """
    update department to db table department by md5-id
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.depart_update(params)


@system.route('/depart_drag/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def depart_drag():
    """
    update department parent node to db table department by md5-id
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.depart_drag(params)


@system.route('/log_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def log_list():
    """
    system > log list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.log_list(params)


@system.route('/avatar_list/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def avatar_list():
    """
    system > avatar list
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.avatar_list(params)


@system.route('/avatar_delete/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def avatar_delete():
    """
    system > delete one avatar data by md5
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.avatar_delete(params)


@system.route('/avatar_deletes/', methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def avatar_deletes():
    """
    system > delete many avatar data by md5 list
    :return: json data
    """
    if request.method in ['GET', 'POST']:
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.avatar_deletes(params)


@system.route('/avatar_detail/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def avatar_detail():
    """
    system > get avatar detail information by md5
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.avatar_detail(params)


@system.route('/avatar_update/', methods=['GET', 'POST'], strict_slashes=False)
@watcher(watcher_args=request)
@watch_except
def avatar_update():
    """
    system > update avatar detail information by md5, contain:
        - name
        - type
        - label
        - summary
        - order_id
    :return: json data
    """
    if request.method == 'GET':
        return Status(
            300, StatusEnum.FAILURE.value, StatusMsgs.get(300), {}).json()

    # 参数
    params = request.get_json() or {}
    return info_service.avatar_update(params)


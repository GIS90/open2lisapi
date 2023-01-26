# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    the view of manage
    主要用于login and logout的api

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    login: 登录
    logout: 退出

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.
------------------------------------------------
"""
from datetime import datetime
from flask import Blueprint, g,\
    request, session, redirect, url_for, jsonify
from flask_cors import CORS

from deploy.utils.logger import logger as LOG
from deploy.utils.utils import get_user_id
from deploy.utils.status import Status
from deploy.services.sysuser import SysUserService
from deploy.services.request import RequestService
from deploy.utils.status_msg import StatusMsgs


manage = Blueprint('manage', __name__, url_prefix='/manage')
CORS(manage, supports_credentials=True)

NoNameBody = 'NoNameBody'
request_service = RequestService()


@manage.route('/login/', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
    login > login in to system
    :return: json data
    """
    if request.method == 'POST':
        # login parameter check
        data_json = request.get_json() or {}
        rtx_id = data_json.get('username')      # 登录账户：支持用户rtx_id、phone、email登录
        user_pwd = data_json.get('password')    # 登录密码
        if not rtx_id:
            return Status(
                212, 'failure', u'缺少username请求参数', {}).json()
        if not user_pwd:
            return Status(
                212, 'failure', u'缺少password请求参数', {}).json()
        # >>>>>>>>>>>>>>>>>>>>> start login <<<<<<<<<<<<<<<<<<<<<
        start = datetime.now()      # start time
        # 支持用户rtx-id、phone、email登录
        rtx_id = rtx_id.strip()  # 去空格
        user_model = SysUserService().get_login_by_rtx(rtx_id)  # 用户多参登录
        # user is not exist
        if not user_model:
            return Status(
                202, 'failure', u'用户未注册，请联系管理员注册' or StatusMsgs.get(202), {}).json()
        # user is deleted
        if user_model.get('is_del'):
            return Status(
                203, 'failure', u'用户已注销，不允许登录系统' or StatusMsgs.get(203), {}).json()
        # check password
        if user_model.get('password') != user_pwd:
            return Status(
                201, 'failure', u'密码不正确，请重新输入密码' or StatusMsgs.get(201), {}
            ).json()
        # check is or not exist token
        if not user_model.get('md5_id'):
            return Status(
                999, 'failure', u'Token初始化失败，请联系管理员', {}).json()
        """ user is login success"""
        rtx_id = user_model.get('rtx_id') or rtx_id
        LOG.info('%s login in <<<<<<<<<<<<<' % rtx_id or NoNameBody)
        session['user-id'] = rtx_id     # 设置用户登录session状态

        end = datetime.now()    # end time
        cost = round((end - start).microseconds * pow(0.1, 6), 4)  # API run time, unit is second
        # watcher打点 >>>>>>>>> request
        request_service.add_request(request=request, cost=cost, rtx=rtx_id)
        return Status(
            100, 'success', StatusMsgs.get(100), {'token': user_model.get('md5_id')}).json()
    else:
        # 不支持其他请求
        return Status(
            211, 'failure', StatusMsgs.get(211), {}).json()


@manage.route('/logout/', methods=['GET', 'POST'], strict_slashes=False)
def logout():
    """
    logout > user login out the system
    :return: json data
    """
    start = datetime.now()
    rtx_id = get_user_id()
    if rtx_id:
        LOG.info('%s login out >>>>>>>>>>>>>' % rtx_id)
    session.clear()     # 清空session状态
    end = datetime.now()
    cost = round((end - start).microseconds * pow(0.1, 6), 4)  # API run time, unit is second
    # watcher打点 >>>>>>>>> request
    request_service.add_request(request=request, cost=cost, rtx=rtx_id)
    return Status(
        100, 'success', StatusMsgs.get(100), {}).json()

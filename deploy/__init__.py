#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    WebFlaskServer initialize 
    flask app and blueprint collections

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    ------------------------------------------------------------------------------
    from deploy import create_app

    app = create_app()

    # 手动启动
    if __name__ == '__main__':
        app.run(host="0.0.0.0", port=9999, debug=True)
    ------------------------------------------------------------------------------

design:
    WebFlaskServer use Singleton mode

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python __init__.py.py
# ------------------------------------------------------------
# three package
import os
import sys
from flask import (Flask,
                   make_response,
                   abort,
                   redirect,
                   url_for,
                   g,
                   request,
                   )

from deploy.config import VERSION, NAME, SECRET_KEY
from deploy.model.base import get_session

# build-in package
from deploy.utils.base_class import WebBaseClass
from deploy.utils.logger import logger as LOG
from deploy.utils.utils import get_user_id, get_real_ip
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum

# view
from deploy.view import add_routers
# service
from deploy.service.sysuser import SysUserService


app = Flask(__name__)
"""
全局CORS跨域，不建议使用
在指定需要跨域的路由中进行配置
服务器允许用户跨源发出Cookie或经过身份验证的请求，supports_credentials设置为True，否则设置False
"""
# from flask_cors import CORS
# CORS(app, supports_credentials=True)


class WebFlaskServer(WebBaseClass):
    app = None
    version = VERSION
    name = NAME

    def __init__(self, app):
        """
        Initialize WebFlaskServer instance, Flask App base configuration
        in addition flask configuration
        """
        # Flask App
        self.app = app
        if not self.app:
            LOG.info('Web server initialize is failure......')
            sys.exit(1)

        # App base configuration
        # -------------------------------------------------------------------------------
        _realpath = os.path.dirname(os.path.realpath(__file__))
        self.app.template_folder = _realpath + '/templates/'
        self.app.secret_key = SECRET_KEY or 'I love python'
        self.app.static_folder = _realpath + '/static'
        self.app.static_url_path = '/static'
        self.app.add_url_rule(self.app.static_url_path + '/<path:filename>',
                              endpoint='static',
                              view_func=self.app.send_static_file)
        self.sysuser_service = SysUserService()
        # -------------------------------------------------------------------------------

        # App webhook
        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        @self.app.before_request
        def before_request():
            # 设置无操作60min，session自动过期
            # session.permanent = True
            # self.app.permanent_session_lifetime = timedelta(minutes=60)

            """
            user was login
            """
            if get_user_id():
                return
            """
            no check condition
            no record request condition
              - api: rest open apis, special api for blueprints
              - access: login in and login out APIs
              - user/info: get user information by token
            """
            # blueprint
            if getattr(request, 'blueprint', None) \
                    and request.blueprint in ['api', 'access']:
                return
            # url>path
            if getattr(request, 'path', None):
                if any([
                    request.path.startswith('/api'),
                    request.path.startswith('/access'),
                    request.path.startswith('/user/info')
                ]):
                    return
            """
            no check condition
            no record request condition
              - ForApi or for_api: special api
            """
            # endpoint
            if getattr(request, 'endpoint', None) and \
                    (request.endpoint.endswith('ForApi')
                     or request.endpoint.endswith('for_api')):
                return
            """
            check current access user is or not legal request
            request require X-Token information at request headers
            X-Token to check legal user by database table sysuser[md5-id]
            legal request && legal user >>>>> access
            otherwise >>>>> no access
            """
            if request.headers.get('X-Token'):      # legal request
                user_model = self.sysuser_service.get_user_by_token(request.headers.get('X-Token'))   # legal user
                if user_model:
                    # new add check request headers[X-Rtx-Id] is or not equal user model[rtx_id]
                    if request.headers.get('X-Rtx-Id') != user_model.get('rtx_id'):
                        return Status(
                            205, StatusEnum.FAILURE.value, "用户Token与当前登录用户不符合", {}).json()

                    return
            # Other condition, user is required login in
            return Status(
                200, StatusEnum.FAILURE.value, '用户未登录', {}).json()

        @self.app.after_request
        def after_request(response):
            """
            在after_request钩子函数中对response进行添加headers
            """
            resp = make_response(response)
            """
            # 跨域
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
            resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
            """
            resp.headers['Content-Type'] = 'application/json;charset=UTF-8'
            return resp

        @self.app.before_first_request
        def before_first_request():
            g._session = get_session()
        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

        # App error handler
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        @self.app.errorhandler(404)
        def not_found_error(error):
            LOG.error(">>>>> [%s] is not found 404" % request.url)
            abort(404)

        @self.app.errorhandler(500)
        def server_error(error):
            LOG.error(">>>>> [%s] is server error 500" % request.url)
            abort(500)
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

        # set favicon
        @self.app.route('/favicon.ico')
        def get_default_favicon():
            return self.app.send_static_file('images/favicon.ico')

        # WebFlaskServer parent class init
        super(WebFlaskServer, self).__init__()

    def __str__(self):
        print("WebFlaskServer class...")

    def __repr__(self):
        self.__str__()

    def register_blueprint(self, blueprint_n, blueprint):
        """
        view blueprint register
        :param blueprint_n: blueprint name
        :param blueprint: blueprint object
        :return: None
        """
        if blueprint:
            LOG.info('Blueprint %s is register.' % blueprint_n)
            self.app.register_blueprint(blueprint)

    def _auto_init_register_blueprint(self):
        for route in add_routers:
            if not route: continue
            self.register_blueprint(route.get('name'), route.get('route'))

    def init_run(self):
        """
        Parent class build-in method
        """
        LOG.debug('Web server is initializing......')
        self._auto_init_register_blueprint()
        LOG.info('Web server is running......')


def create_app():
    return WebFlaskServer(app).app

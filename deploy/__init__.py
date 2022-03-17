#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    WebFlaskServer initialize 
    flask app and blueprint collections
    
    Singleton mode

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "twtoolbox_isapi"

usage:

design:

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
import os
import sys
from datetime import timedelta
from flask import (Flask,
                   abort,
                   redirect,
                   url_for,
                   g,
                   request)

from deploy.config import VERSION, NAME, SECRET_KEY
from deploy.models.base import get_session
from deploy.utils.base_class import WebBaseClass
from deploy.utils.logger import logger as LOG
from deploy.utils.utils import get_user_id, timeer, get_real_ip
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs

from deploy.views.manage import manage
from deploy.views.user import user
from deploy.services.sysuser import SysUserService
from deploy.services.request import RequestService


app = Flask(__name__)
"""
全局CORS跨域，不建议使用
在指定需要跨域的路由中进行配置
"""
# from flask_cors import CORS
# CORS(app, supports_credentials=True)


class WebFlaskServer(WebBaseClass):
    app = None
    version = VERSION
    name = NAME

    def __init__(self, app):
        """
        Initialize webFlaskServer instance
        and flask configuration
        """
        self.app = app
        if not self.app:
            LOG.info('Web server initialize is failure......')
            sys.exit(1)

        _realpath = os.path.dirname(os.path.realpath(__file__))
        self.app.template_folder = _realpath + '/templates/'
        self.app.secret_key = SECRET_KEY or 'python'
        self.app.static_folder = _realpath + '/static'
        self.app.static_url_path = '/static'
        self.app.add_url_rule(self.app.static_url_path + '/<path:filename>',
                              endpoint='static',
                              view_func=self.app.send_static_file)
        self.request_service = RequestService()
        super(WebFlaskServer, self).__init__()

        @self.app.before_request
        def before_request():
            # 设置无操作60min，session自动过期
            # session.permanent = True
            # self.app.permanent_session_lifetime = timedelta(minutes=60)

            if get_user_id():
                return
            """
            apis: rest apis
            ForApi or for_api: special api
            """
            if request.blueprint in ['apis', 'manage']:
                return
            """
            special api for blueprints
            """
            if request.endpoint and \
                    (request.endpoint.endswith('ForApi')
                     or request.endpoint.endswith('for_api')):
                return
            """
            record access and use system function
            X-Token
            """
            if request.headers.get('X-Token'):
                user_model = SysUserService().\
                    get_user_by_token(request.headers.get('X-Token'))
                if user_model:
                    self.request_service.add_request(request)  # 加入请求API日志
                    return

            return Status(
                200,
                'failure',
                StatusMsgs.get(200) or u'用户未登录',
                {}
            ).json()

        @self.app.before_first_request
        def before_first_request():
            g._session = get_session()

        @self.app.errorhandler(404)
        def not_found_error(error):
            LOG.error("%s is not found 404" % request.url)
            abort(404)

        @self.app.errorhandler(500)
        def server_error(error):
            LOG.error("%s is server error 500" % request.url)
            abort(500)

        # set favicon
        @self.app.route('/favicon.ico')
        def get_default_favicon():
            return self.app.send_static_file('images/favicon.ico')

    def register_blueprint(self, obj_n, obj):
        """
        view blueprint register
        :param obj_n: blueprint object
        :param obj: blueprint name
        :return: None
        """
        if obj:
            LOG.info('Blueprint %s is register' % obj_n)
            self.app.register_blueprint(obj)

    def _autoinit_register_blueprint(self):
        self.register_blueprint('manage', manage)
        self.register_blueprint('user', user)

    def init_run(self):
        LOG.debug('Server is initializing......')
        self._autoinit_register_blueprint()
        LOG.info('Web server is running......')


def create_app():
    return WebFlaskServer(app).app

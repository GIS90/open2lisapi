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
    __project__ = "open2lisapi"

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
from flask import (Flask, make_response,
                   abort,
                   redirect,
                   url_for,
                   g,
                   request)

from deploy.config import VERSION, NAME, SECRET_KEY
from deploy.models.base import get_session
# build-in package
from deploy.utils.base_class import WebBaseClass
from deploy.utils.logger import logger as LOG
from deploy.utils.utils import get_user_id, timeer, get_real_ip
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
# views
from deploy.views.manage import manage
from deploy.views.user import user
from deploy.views.office import office
from deploy.views.authority import auth
from deploy.views.notify import notify
from deploy.views.common import common
from deploy.views.dashboard import dashboard
from deploy.views.system import system
from deploy.views.search import search
from deploy.views.image import image
from deploy.views.apis import apis
# services
from deploy.services.sysuser import SysUserService
from deploy.services.request import RequestService


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
        Initialize webFlaskServer instance
        and flask configuration
        """
        self.app = app
        if not self.app:
            LOG.info('Web server initialize is failure......')
            sys.exit(1)
        # flask base config
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

            """
            user is logined in
            """
            if get_user_id():
                return
            """
            no check condition
            no record request condition
              - apis: rest open apis, special api for blueprints
              - manage: login in and login out APIs
            """
            if request.blueprint in ['apis', 'manage']:
                return
            """
            no check condition
            no record request condition
              - ForApi or for_api: special api
            """
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
                user_model = SysUserService().\
                    get_user_by_token(request.headers.get('X-Token'))   # legal user
                if user_model:
                    # change watcher to hit point
                    """
                    try:
                        self.request_service.add_request(request)  # 加入请求API日志
                    except: pass
                    """
                    return
            # Other condition, user is required login in
            return Status(
                200, 'failure', StatusMsgs.get(200) or u'用户未登录', {}).json()

        """
        @self.app.after_request
        def after_request(response):
            '''
            在after_request钩子函数中对response进行添加headers，所有的url跨域请求都会允许。。。
            '''
            resp = make_response(response)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
            resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
            return resp
        """
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
        :param obj_n: blueprint name
        :param obj: blueprint object
        :return: None
        """
        if obj:
            LOG.info('Blueprint %s is register' % obj_n)
            self.app.register_blueprint(obj)

    def _autoinit_register_blueprint(self):
        self.register_blueprint('dashboard', dashboard)
        self.register_blueprint('manage', manage)
        self.register_blueprint('user', user)
        self.register_blueprint('common', common)
        self.register_blueprint('search', search)
        self.register_blueprint('office', office)
        self.register_blueprint('notify', notify)
        self.register_blueprint('system', system)
        self.register_blueprint('auth', auth)
        self.register_blueprint('image', image)
        self.register_blueprint('apis', apis)

    def init_run(self):
        LOG.debug('Server is initializing......')
        self._autoinit_register_blueprint()
        LOG.info('Web server is running......')


def create_app():
    return WebFlaskServer(app).app

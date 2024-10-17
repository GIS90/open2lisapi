#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    the run configuration information of the project
    use analyse to the config of yaml formatter
    information:
        - SERVER
        - LOG
        - DB
        - MAIL
        - FILES: upload file or ...

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/5/20 10:00 AM"
    __mail__ = "mingliang.gao@163.com"

remark:
    2024.10.08 update：采用pathlib方式

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python config.py
# ------------------------------------------------------------
import os
import sys
import yaml
import logging
from pathlib import Path


# config file absolute path
config_abspath_file = Path(__file__).resolve()
if not config_abspath_file.is_absolute():
    _os_path = os.path.dirname(os.path.abspath(__file__))
    config_abspath_file = Path(_os_path)
# logging.basicConfig()
logger = logging.getLogger(__name__)


# get deploy folder, solve is or not frozen of the script
def _get_deploy_folder():
    return config_abspath_file.parent


# get deploy folder, solve is or not frozen of the script
def _get_root_folder():
    return _get_deploy_folder().parent


# get current run config by mode
def _get_config(mode='dev'):
    # not allow mode parameters
    if mode not in ['dev', 'prod']:
        return None
    # root path is not abs
    root = _get_root_folder()
    if not root.is_absolute():
        return None

    return root.joinpath('etc').joinpath(mode).joinpath('config.yaml')


# default log dir
def _get_log_folder():
    root = _get_root_folder()
    if not root.is_absolute():
        return None

    return root.joinpath('log')


"""~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ !"""


"""
default config
avoid initialization parameters is empty
"""
# SERVER
NAME = 'Open2L----->'
VERSION = 'v1.0.0'
DEBUG = True
SECRET_KEY = 'IbelivemeIcanfly-gaomingliang'
ADMIN = 'admin'
ADMIN_AUTH_LIST = []

# DB(sqlalchemy)，default is mysql
DB_LINK = None

# LOG
LOG_DIR = _get_log_folder()
LOG_LEVEL = "debug"
LOG_FORMATTER = "%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s - %(message)s"
LOG_FILENAME_PREFIX = 'base_webframe'

# mail
MAIL_SERVER = None
MAIL_PORT = None
MAIL_USE_SSL = None
MAIL_USERNAME = None
MAIL_PASSWORD = None

# user
USER_DEFAULT_AVATAR = 'http://pygo2.top/images/article_w.jpg'
USER_DEFAULT_PASSWORD = 'abc1234'
USER_DEFAULT_TIMELINE = 6
USER_DEFAULT_INTROD = "这家伙很懒，什么也没留下......"
USER_AVATAR_STORE_URL = "http://avatar.pygo2.top"
USER_AVATAR_STORE_NAME = "avatar-default"

# store
_CACHE = '/deploy/static/cache'
STORE_BASE_URL = 'http://store.pygo2.top'
STORE_ACCESS = 'mRF0cKGUJcfv7ry_Wyvc24cDNWEQz9DAKo_UOn0G'
STORE_SECRET = 'xabmlB9zZ_MRwtgofQJzUxINnmcO_VUfkXYILx_Q'
STORE_SPACE_NAME = 'open2lisapi'

# menu
MENU_ROOT_ID = 1
MENU_ROOT_LEVEL = 0
MENU_ONE_LEVEL = 1

# image
IMAGE_QUALITY = 100
IMAGE_WIDTH = 1000

# article
ART_LIMIT = 10

# office
OFFICE_LIMIT = 15
OFFICE_STORE_BK = False
SHEET_NUM_LIMIT = 20
SHEET_NAME_LIMIT = 85

# convert
CONVERT_MULPRO = True

# authority
AUTH_LIMIT = 15
AUTH_NUM = 45

# DINGTALK
DTALK_BASE_URL = 'https://oapi.dingtalk.com/'
DTALK_TOKEN_URL = 'gettoken'
DTALK_TITLE = True
DTALK_ADD_IMAGE = ''
DTALK_CONTROL = []
DTALK_INTERVAL = 0.5

# QYWX企业微信
QYWX_BASE_URL = 'https://qyapi.weixin.qq.com'
QYWX_ACCESS_TOKEN = '/cgi-bin/gettoken'
QYWX_SEND_MESSAGE = '/cgi-bin/message/send'
QYWX_SEND_BACK = '/cgi-bin/message/recall'
QYWX_TEMP_UPLOAD = '/cgi-bin/media/upload'
QYWX_TEMP_GET = '/cgi-bin/media/get'

# DEPART部门树
DEPART_ROOT_ID = 1
DEPART_ROOT_PID = 0

# jwt token
JWT_TOKEN_SECRET_KEY = "Enjoy the good life everyday！！!"  # 密钥
JWT_TOKEN_ALGORITHM = "HS256"  # 算法
JWT_TOKEN_EXPIRE_MINUTES = 60 * 4   # 访问令牌过期时间，单位：分

# others
NOBN = 'NoNameBody'

"""
Entry: initialize config
"""
mode = os.environ.get('mode') or 'dev'
_config_file = _get_config(mode)
if not os.path.exists(_config_file):
    logger.critical('====== config file is not exist, exit ======')
    sys.exit(1)

with open(_config_file, 'r', encoding='UTF-8') as f:
    _config_info = yaml.safe_load(f)
    if not _config_info:
        logger.critical('====== config file is unavail, exit ======')
        sys.exit(1)

    # SERVER
    NAME = _config_info['SERVER']['NAME'] or NAME
    VERSION = _config_info['SERVER']['VERSION'] or VERSION
    DEBUG = _config_info['SERVER']['DEBUG'] or DEBUG
    SECRET_KEY = _config_info['SERVER']['SECRET_KEY'] or SECRET_KEY
    ADMIN = _config_info['SERVER']['ADMIN'] or ADMIN
    ADMIN_AUTH_LIST = _config_info['SERVER']['ADMIN_AUTH_LIST'] or ADMIN_AUTH_LIST

    # DB(sqlalchemy)，default is mysql
    DB_LINK = _config_info['DB']['DB_LINK'] or DB_LINK

    # LOG
    if _config_info['LOG']['LOG_DIR']:
        LOG_DIR = os.path.join(os.path.dirname(_get_deploy_folder()), _config_info['LOG']['LOG_DIR'])
    else:
        LOG_DIR = LOG_DIR
    if not os.path.exists(LOG_DIR):
        logger.critical('====== log dir is not exist, create %s... ======' % LOG_DIR)
        os.makedirs(LOG_DIR)
    LOG_LEVEL = _config_info['LOG']['LOG_LEVEL'] or LOG_LEVEL
    LOG_FORMATTER = _config_info['LOG']['LOG_FORMATTER'] or LOG_FORMATTER
    LOG_FILENAME_PREFIX = _config_info['LOG']['LOG_FILENAME_PREFIX'] or LOG_FILENAME_PREFIX

    # mail
    MAIL_SERVER = _config_info['MAIL']['MAIL_SERVER'] or MAIL_SERVER
    MAIL_PORT = int(_config_info['MAIL']['MAIL_PORT']) or MAIL_PORT
    MAIL_USE_SSL = _config_info['MAIL']['MAIL_USE_SSL'] or MAIL_USE_SSL
    MAIL_USERNAME = _config_info['MAIL']['MAIL_USERNAME'] or MAIL_USERNAME
    MAIL_PASSWORD = _config_info['MAIL']['MAIL_PASSWORD'] or MAIL_PASSWORD

    # user info
    USER_DEFAULT_AVATAR = _config_info['USER']['AVATAR'] or USER_DEFAULT_AVATAR
    USER_DEFAULT_PASSWORD = _config_info['USER']['PASSWORD'] or USER_DEFAULT_PASSWORD
    USER_DEFAULT_TIMELINE = _config_info['USER']['TIMELINE'] or USER_DEFAULT_TIMELINE
    USER_DEFAULT_INTROD = _config_info['USER']['INTRODUCTION'] or USER_DEFAULT_INTROD
    USER_AVATAR_STORE_URL = _config_info['USER']['STORE_BASE_URL'] or USER_AVATAR_STORE_URL
    USER_AVATAR_STORE_NAME = _config_info['USER']['STORE_NAME'] or USER_AVATAR_STORE_NAME

    # store
    STORE_BASE_URL = _config_info['STORE']['BASE_URL'] or STORE_BASE_URL
    STORE_ACCESS = _config_info['STORE']['ACCESS'] or STORE_ACCESS
    STORE_SECRET = _config_info['STORE']['SECRET'] or STORE_SECRET
    STORE_SPACE_NAME = _config_info['STORE']['SPACE_NAME'] or STORE_SPACE_NAME
    if _config_info['STORE']['CACHE']:
        STORE_CACHE = _config_info['STORE']['CACHE']
    else:
        STORE_CACHE = os.path.join(os.path.dirname(_get_deploy_folder()), _CACHE)
    if not os.path.exists(STORE_CACHE):
        logger.critical('====== store dir is not exist, create %s... ======' % STORE_CACHE)
        os.makedirs(STORE_CACHE)

    # menu
    MENU_ROOT_ID = _config_info['MENU']['MENU_ROOT_ID'] or MENU_ROOT_ID
    MENU_ROOT_LEVEL = _config_info['MENU']['MENU_ROOT_LEVEL'] or MENU_ROOT_LEVEL
    MENU_ONE_LEVEL = _config_info['MENU']['MENU_ONE_LEVEL'] or MENU_ONE_LEVEL

    # image
    IMAGE_QUALITY = _config_info['IMAGE']['QUALITY'] or IMAGE_QUALITY
    IMAGE_WIDTH = _config_info['IMAGE']['WIDTH'] or IMAGE_WIDTH

    # article
    ART_LIMIT = _config_info['ARTICLE']['LIMIT'] or ART_LIMIT

    # office
    OFFICE_LIMIT = _config_info['OFFICE']['LIMIT'] or OFFICE_LIMIT
    OFFICE_STORE_BK = _config_info['OFFICE']['STORE_BK'] or OFFICE_STORE_BK
    SHEET_NUM_LIMIT = _config_info['OFFICE']['SHEET_NUM_LIMIT'] or SHEET_NUM_LIMIT
    SHEET_NAME_LIMIT = _config_info['OFFICE']['SHEET_NAME_LIMIT'] or SHEET_NAME_LIMIT

    # convert
    CONVERT_MULPRO = _config_info['CONVERT']['MULPRO'] or CONVERT_MULPRO

    # authority
    AUTH_LIMIT = _config_info['AUTH']['LIMIT'] or AUTH_LIMIT
    AUTH_NUM = _config_info['AUTH']['NUM'] or AUTH_NUM

    # options
    O_NOBN = _config_info['OTHERS']['NOBN'] or NOBN

    # DINGTALK
    DTALK_BASE_URL = _config_info['DINGTALK']['BASE_URL'] or DTALK_BASE_URL
    DTALK_TOKEN_URL = _config_info['DINGTALK']['TOKEN_URL'] or DTALK_TOKEN_URL
    DTALK_TITLE = _config_info['DINGTALK']['TITLE'] or DTALK_TITLE
    DTALK_ADD_IMAGE = _config_info['DINGTALK']['ADD_IMAGE'] or DTALK_ADD_IMAGE
    DTALK_CONTROL = _config_info['DINGTALK']['CONTROL'] or DTALK_CONTROL
    DTALK_INTERVAL = _config_info['DINGTALK']['INTERVAL'] or DTALK_INTERVAL

    # QYWX
    QYWX_BASE_URL = _config_info['QYWX']['BASE_URL'] or QYWX_BASE_URL
    QYWX_ACCESS_TOKEN = _config_info['QYWX']['ACCESS_TOKEN'] or QYWX_ACCESS_TOKEN
    QYWX_SEND_MESSAGE = _config_info['QYWX']['SEND_MESSAGE'] or QYWX_SEND_MESSAGE
    QYWX_SEND_BACK = _config_info['QYWX']['SEND_BACK'] or QYWX_SEND_BACK
    QYWX_TEMP_UPLOAD = _config_info['QYWX']['TEMP_UPLOAD'] or QYWX_TEMP_UPLOAD
    QYWX_TEMP_GET = _config_info['QYWX']['TEMP_GET'] or QYWX_TEMP_GET

    # depart
    DEPART_ROOT_ID = _config_info['DEPART']['ROOT_ID'] or DEPART_ROOT_ID
    DEPART_ROOT_PID = _config_info['DEPART']['ROOT_PID'] or DEPART_ROOT_PID

    # JWT
    JWT_TOKEN_SECRET_KEY = _config_info['JWT']['KEY'] or JWT_TOKEN_SECRET_KEY
    JWT_TOKEN_ALGORITHM = _config_info['JWT']['ALGORITHM'] or JWT_TOKEN_ALGORITHM
    JWT_TOKEN_EXPIRE_MINUTES = int(_config_info['JWT']['EXPIRE']) or JWT_TOKEN_EXPIRE_MINUTES

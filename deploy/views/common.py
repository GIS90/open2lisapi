# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    common apis

base_info:
    __author__ = "PyGo"
    __time__ = "2022/6/10 22:41"
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
# usage: /usr/bin/python common.py
# ------------------------------------------------------------
from flask import Blueprint, request
from flask_cors import CORS, cross_origin


common = Blueprint('common', __name__, url_prefix='/common')
CORS(common, supports_credentials=True)

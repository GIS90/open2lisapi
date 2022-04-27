# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/4/27 3:03 下午"
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
# usage: /usr/bin/python excel_result.py
# ------------------------------------------------------------

from deploy.bo.bo_base import BOBase
from deploy.models.excel_result import ExcelResultModel


class ExcelResultBo(BOBase):

    def __init__(self):
        super(ExcelResultBo, self).__init__()

    def new_mode(self):
        return ExcelResultModel()

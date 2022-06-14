# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/6/14 22:17"
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
# usage: /usr/bin/python office.py
# ------------------------------------------------------------

from deploy.bo.bo_base import BOBase
from deploy.models.office import OfficeModel


class OfficeBo(BOBase):

    def __init__(self):
        super(OfficeBo, self).__init__()

    def new_mode(self):
        return OfficeModel()

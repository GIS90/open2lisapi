# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/22 11:08 上午"
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

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python menu.py
# ------------------------------------------------------------
from sqlalchemy import or_

from deploy.bo.bo_base import BOBase
from deploy.models.enum import EnumModel


class EnumBo(BOBase):

    def __init__(self):
        super(EnumBo, self).__init__()

    def new_mode(self):
        return EnumModel()

    def get_model_by_name(self, name):
        if not name:
            return None
        q = self.session.query(EnumModel)
        q = q.filter(EnumModel.name == name)
        q = q.filter(EnumModel.is_del != True)
        q = q.order_by(EnumModel.id.asc())
        q = q.all()
        return q

    def get_model_by_names(self, names):
        if not names:
            return None
        q = self.session.query(EnumModel)
        q = q.filter(EnumModel.name.in_(names))
        q = q.filter(EnumModel.is_del != True)
        q = q.order_by(EnumModel.id.asc())
        q = q.all()
        return q
# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/8/25 21:40"
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
# usage: /usr/bin/python shortcut.py
# ------------------------------------------------------------
from sqlalchemy import or_

from deploy.bo.bo_base import BOBase
from deploy.model.shortcut import ShortCutModel


class ShortCutBo(BOBase):

    def __init__(self):
        super(ShortCutBo, self).__init__()

    def new_mode(self):
        return ShortCutModel()

    def execute_sql(self, sql):
        if not sql:
            return None
        q = self.session.execute(sql)
        return q

    def get_model_by_rtx(self, rtx):
        if not rtx:
            return None
        q = self.session.query(ShortCutModel)
        q = q.filter(ShortCutModel.rtx_id == str(rtx))
        return q.first()

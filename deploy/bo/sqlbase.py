# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/12/21 20:39"
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
# usage: /usr/bin/python sqlbase.py
# ------------------------------------------------------------
from sqlalchemy import distinct, func

from deploy.bo.bo_base import BOBase
from deploy.models.sqlbase import SqlbaseModel


class SqlbaseBo(BOBase):

    def __init__(self):
        super(SqlbaseBo, self).__init__()

    def new_mode(self):
        return SqlbaseModel()

    def execute_sql(self, sql):
        if not sql:
            return None
        q = self.session.execute(sql)
        return q

    def get_all(self, params: dict):
        q = self.session.query(SqlbaseModel)
        q = q.filter(SqlbaseModel.is_del != 1)
        if params.get('public'):
            q = q.filter(SqlbaseModel.public == True)
        if not params.get('public'):
            q = q.filter(SqlbaseModel.public == False)
        if params.get('rtx_id'):
            q = q.filter(SqlbaseModel.rtx_id == str(params.get('rtx_id')))
        q = q.order_by(SqlbaseModel.create_time.desc())
        if not q:
            return [], 0
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total


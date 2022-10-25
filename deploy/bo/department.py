# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/10/11 21:22"
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
# usage: /usr/bin/python department.py
# ------------------------------------------------------------
from sqlalchemy import distinct, func

from deploy.bo.bo_base import BOBase
from deploy.models.department import DepartmentModel


class DepartmentBo(BOBase):

    def __init__(self):
        super(DepartmentBo, self).__init__()

    def new_mode(self):
        return DepartmentModel()

    def execute_sql(self, sql):
        if not sql:
            return None
        q = self.session.execute(sql)
        return q

    def get_all(self, root=False):
        q = self.session.query(DepartmentModel)
        if not root:
            q = q.filter(DepartmentModel.id != 1)
        q = q.filter(DepartmentModel.is_del != True)
        q = q.order_by(DepartmentModel.order_id.asc(), DepartmentModel.id.asc())
        q = q.all()
        return q

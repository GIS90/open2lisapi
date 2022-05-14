# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    role bo

base_info:
    __author__ = "PyGo"
    __time__ = "2022/5/9 23:00"
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
# usage: /usr/bin/python role.py
# ------------------------------------------------------------
from sqlalchemy import or_

from deploy.bo.bo_base import BOBase
from deploy.models.role import RoleModel


class RoleBo(BOBase):

    def __init__(self):
        super(RoleBo, self).__init__()

    def new_mode(self):
        return RoleModel()

    def get_all(self, params):
        q = self.session.query(RoleModel)
        q = q.filter(RoleModel.is_del != True)
        if not q:
            return [], 0
        total = len(q.all())
        q = q.order_by(RoleModel.create_time.desc())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

    def get_model_by_engname(self, engname):
        if not engname:
            return None
        q = self.session.query(RoleModel)
        q = q.filter(RoleModel.engname == engname)
        q = q.filter(RoleModel.is_del != True)
        return q.first()

    def get_model_by_engname_nodel(self, engname):
        if not engname:
            return None
        q = self.session.query(RoleModel)
        q = q.filter(RoleModel.engname == engname)
        return q.first()

    def get_model_by_md5(self, md5):
        if not md5:
            return None
        q = self.session.query(RoleModel)
        q = q.filter(RoleModel.md5_id == md5)
        return q.first()
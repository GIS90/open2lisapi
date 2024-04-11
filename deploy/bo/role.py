# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    Role Bo

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
from deploy.model.role import RoleModel

from deploy.utils.utils import get_now


class RoleBo(BOBase):

    def __init__(self):
        super(RoleBo, self).__init__()

    def __str__(self):
        return "Role Bo."

    def __repr__(self):
        return self.__str__()

    def new_mode(self):
        return RoleModel()

    def get_all(self, params):
        q = self.session.query(RoleModel)
        q = q.filter(RoleModel.is_del != True)
        # 选择下载条件
        if params.get('list'):
            q = q.filter(RoleModel.md5_id.in_(params.get('list')))
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

    def get_models_by_md5list(self, md5_list):
        if not md5_list:
            return []
        q = self.session.query(RoleModel)
        q = q.filter(RoleModel.md5_id.in_(md5_list))
        q = q.filter(RoleModel.is_del != 1)
        return q.all()

    def batch_delete_by_md5(self, params):
        if not params.get('list'):
            return 0

        md5_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(RoleModel)
        q = q.filter(RoleModel.md5_id.in_(md5_list))
        if rtx_id:
            q = q.filter(RoleModel.create_rtx == rtx_id)
        q = q.filter(RoleModel.is_del != 1)
        q = q.update({RoleModel.is_del: True,
                      RoleModel.delete_rtx: rtx_id,
                      RoleModel.delete_time: get_now()},
                     synchronize_session=False)
        return q

    def get_models_by_engnames(self, engname_list):
        if not engname_list:
            return []
        q = self.session.query(RoleModel)
        q = q.filter(RoleModel.engname.in_(engname_list))
        q = q.filter(RoleModel.is_del != True)
        return q.all()

    def get_select_all(self):
        q = self.session.query(RoleModel)
        q = q.filter(RoleModel.is_del != True)
        return q.all()

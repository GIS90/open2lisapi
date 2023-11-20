# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    Enum Bo

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
from sqlalchemy import or_, distinct

from deploy.bo.bo_base import BOBase
from deploy.model.enum import EnumModel
from deploy.utils.utils import get_now


class EnumBo(BOBase):

    def __init__(self):
        super(EnumBo, self).__init__()

    def __str__(self):
        return "Enum Bo."

    def __repr__(self):
        return self.__str__()

    def new_mode(self):
        return EnumModel()

    def get_all(self, params):
        q = self.session.query(EnumModel)
        q = q.filter(EnumModel.is_del != 1)     # 过滤删除
        q = q.order_by(EnumModel.name.asc(), EnumModel.order_id.asc())      # name, order_id 排序
        if not q:
            return [], 0
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

    def get_model_by_name(self, name):
        if not name:
            return None
        q = self.session.query(EnumModel)
        q = q.filter(EnumModel.name == name)
        q = q.filter(EnumModel.status != False)
        q = q.filter(EnumModel.is_del != True)
        # q = q.order_by(EnumModel.id.asc())
        q = q.order_by(EnumModel.order_id.asc())
        q = q.all()
        return q

    def get_model_by_names(self, names):
        if not names:
            return None
        q = self.session.query(EnumModel)
        q = q.filter(EnumModel.name.in_(names))
        q = q.filter(EnumModel.status != False)
        q = q.filter(EnumModel.is_del != True)
        q = q.order_by(EnumModel.order_id.asc())
        q = q.all()
        return q

    def get_model_by_md5(self, md5_id):
        q = self.session.query(EnumModel)
        q = q.filter(EnumModel.md5_id == md5_id)
        return q.first()

    def batch_delete_by_md5(self, params):
        # no md5 list, return 0
        if not params.get('list'):
            return 0

        md5_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(EnumModel)
        q = q.filter(EnumModel.md5_id.in_(md5_list))
        q = q.filter(EnumModel.is_del != 1)     # only delete is_del is False
        q = q.update({EnumModel.is_del: True,
                      EnumModel.delete_rtx: rtx_id,
                      EnumModel.delete_time: get_now()},
                     synchronize_session=False)
        return q

    def batch_disable_by_md5(self, params):
        # no md5 list, return 0
        if not params.get('list'):
            return 0

        md5_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(EnumModel)
        q = q.filter(EnumModel.md5_id.in_(md5_list))
        # q = q.filter(EnumModel.is_del != 1)     # filter: is or not deleted
        q = q.update({EnumModel.status: False,
                      EnumModel.update_rtx: rtx_id,
                      EnumModel.update_time: get_now()},
                     synchronize_session=False)
        return q

    def enum_group_by_name(self):
        q = self.session.query(distinct(EnumModel.name)).all()
        return q

    def get_add_model_by_name(self, name):
        q = self.session.query(EnumModel)
        q = q.filter(EnumModel.name == str(name))
        q = q.all()
        return q

    def get_model_by_name_key(self, name, key):
        q = self.session.query(EnumModel)
        q = q.filter(EnumModel.name == str(name))
        q = q.filter(EnumModel.key == str(key))
        q = q.filter(EnumModel.is_del != 1)
        q = q.all()
        return q
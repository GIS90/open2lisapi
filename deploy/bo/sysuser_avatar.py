# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    SysUserAvatar Bo

base_info:
    __author__ = "PyGo"
    __time__ = "2023/7/24 07:16"
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
# usage: /usr/bin/python sysuser_avatar.py
# ------------------------------------------------------------
from deploy.utils.utils import get_now
from sqlalchemy import distinct, func

from deploy.bo.bo_base import BOBase
from deploy.model.sysuser_avatar import SysUserAvatarModel


class SysUserAvatarBo(BOBase):

    def __init__(self):
        super(SysUserAvatarBo, self).__init__()

    def __str__(self):
        return "SysUserAvatar Bo."

    def __repr__(self):
        return self.__str__()

    def new_mode(self):
        return SysUserAvatarModel()

    def get_all(self, params: dict):
        q = self.session.query(SysUserAvatarModel)
        q = q.filter(SysUserAvatarModel.is_del != 1)
        if params.get('rtx_id'):
            q = q.filter(SysUserAvatarModel.rtx_id == str(params.get('rtx_id')))
        q = q.order_by(SysUserAvatarModel.order_id.asc(), SysUserAvatarModel.create_time.desc())
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

    def get_model_by_md5(self, md5):
        q = self.session.query(SysUserAvatarModel)
        q = q.filter(SysUserAvatarModel.is_del != 1)
        q = q.filter(SysUserAvatarModel.md5_id == md5)
        return q.first() if q else None

    def batch_delete_by_md5(self, params):
        if not params.get('list'):
            return 0

        md5_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(SysUserAvatarModel)
        q = q.filter(SysUserAvatarModel.md5_id.in_(md5_list))
        q = q.filter(SysUserAvatarModel.is_del != 1)
        q = q.update({SysUserAvatarModel.is_del: True,
                      SysUserAvatarModel.delete_rtx: rtx_id,
                      SysUserAvatarModel.delete_time: get_now()},
                     synchronize_session=False)
        return q

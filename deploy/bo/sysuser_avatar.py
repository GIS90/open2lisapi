# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    sysuser_avatar bo

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
from sqlalchemy import distinct, func

from deploy.bo.bo_base import BOBase
from deploy.models.sysuser_avatar import SysUserAvatarModel


class SysUserAvatarModelBo(BOBase):

    def __init__(self):
        super(SysUserAvatarModelBo, self).__init__()

    def new_mode(self):
        return SysUserAvatarModelBo()

    def execute_sql(self, sql):
        if not sql:
            return None
        q = self.session.execute(sql)
        return q

    def get_all(self, params: dict):
        q = self.session.query(SysUserAvatarModel)
        q = q.filter(SysUserAvatarModel.is_del != 1)
        if params.get('rtx_id'):
            q = q.filter(SysUserAvatarModel.rtx_id == str(params.get('rtx_id')))
        q = q.order_by(SysUserAvatarModel.order_id.asc(), SysUserAvatarModel.create_time.desc())
        if not q:
            return [], 0
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

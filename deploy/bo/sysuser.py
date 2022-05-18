# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    the db interact services of sysuser

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
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
from sqlalchemy import or_

from deploy.bo.bo_base import BOBase
from deploy.models.sysuser import SysUserModel

from deploy.config import ADMIN


class SysUserBo(BOBase):

    def __init__(self):
        super(SysUserBo, self).__init__()

    def new_mode(self):
        return SysUserModel()

    def get_user_by_params(self, user_id):
        if not user_id:
            return None
        q = self.session.query(SysUserModel)
        q = q.filter(or_(SysUserModel.rtx_id == user_id,
                         SysUserModel.email == user_id,
                         SysUserModel.phone == user_id))
        return q.first() if q.first() else None

    def get_user_by_rtx_id(self, rtx_id):
        if not rtx_id:
            return None
        q = self.session.query(SysUserModel)
        q = q.filter(SysUserModel.rtx_id == rtx_id)
        return q.first() if q.first() else None

    def get_user_by_token(self, token):
        if not token:
            return None
        q = self.session.query(SysUserModel)
        q = q.filter(SysUserModel.md5_id == token)
        return q.first() if q.first() else None

    def get_auth_by_rtx(self, rtx_id):
        if not rtx_id:
            return None
        q = self.session.query(SysUserModel)
        q = q.filter(SysUserModel.rtx_id == rtx_id)
        return q.first() if q.first() else None

    def get_all(self, params, is_admin=False):
        q = self.session.query(SysUserModel)
        if not is_admin:
            q = q.filter(SysUserModel.rtx_id != ADMIN)
        if not q:
            return [], 0
        total = len(q.all())
        q = q.order_by(SysUserModel.create_time.desc())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

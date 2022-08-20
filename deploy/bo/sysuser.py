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
from deploy.utils.utils import get_now


class SysUserBo(BOBase):

    def __init__(self):
        super(SysUserBo, self).__init__()

    def new_mode(self):
        return SysUserModel()

    def execute_sql(self, sql):
        if not sql:
            return None
        q = self.session.execute(sql)
        return q

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

    def get_models_by_md5_list(self, md5_list):
        if not md5_list:
            return []
        q = self.session.query(SysUserModel)
        q = q.filter(SysUserModel.md5_id.in_(md5_list))
        return q.all()

    def batch_delete_by_md5_list(self, params):
        if not params.get('list'):
            return 0

        rtx_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(SysUserModel)
        q = q.filter(SysUserModel.md5_id.in_(rtx_list))
        q = q.filter(SysUserModel.is_del != 1)
        q = q.update({SysUserModel.is_del: True,
                      SysUserModel.delete_rtx: rtx_id,
                      SysUserModel.delete_time: get_now()},
                     synchronize_session=False)
        return q

    def get_user_by_phone(self, phone):
        if not phone:
            return None
        q = self.session.query(SysUserModel)
        q = q.filter(SysUserModel.phone == phone)
        return q.first() if q.first() else None

    def get_user_by_email(self, email):
        if not email:
            return None
        q = self.session.query(SysUserModel)
        q = q.filter(SysUserModel.email == email)
        return q.first() if q.first() else None

    def get_count(self, is_del=False, is_admin=False):
        q = self.session.query(SysUserModel)
        if not is_del:
            q = q.filter(SysUserModel.is_del != 1)
        if not is_admin:
            q = q.filter(SysUserModel.rtx_id != ADMIN)
        return len(q.all())

# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/7/27 21:52"
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
# usage: /usr/bin/python dtalk_robot.py
# ------------------------------------------------------------
from sqlalchemy import or_

from deploy.bo.bo_base import BOBase
from deploy.models.dtalk_robot import DtalkRobotModel
from deploy.utils.utils import get_now


class DtalkRobotBo(BOBase):

    def __init__(self):
        super(DtalkRobotBo, self).__init__()

    def new_mode(self):
        return DtalkRobotModel()

    def execute_sql(self, sql):
        if not sql:
            return None
        q = self.session.execute(sql)
        return q

    def get_all(self, params: dict):
        q = self.session.query(DtalkRobotModel)
        q = q.filter(DtalkRobotModel.is_del != 1)
        if params.get('rtx_id'):
            q = q.filter(DtalkRobotModel.rtx_id == str(params.get('rtx_id')))
        q = q.order_by(DtalkRobotModel.create_time.desc())
        if not q:
            return [], 0
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

    def get_model_by_md5(self, md5):
        q = self.session.query(DtalkRobotModel)
        q = q.filter(DtalkRobotModel.md5_id == str(md5))
        return q.first() if q else None

    def get_model_by_key_secret(self, key, secret, rtx_id):
        q = self.session.query(DtalkRobotModel)
        q = q.filter(DtalkRobotModel.key == str(key))
        q = q.filter(DtalkRobotModel.secret == str(secret))
        q = q.filter(DtalkRobotModel.rtx_id == str(rtx_id))
        q = q.filter(DtalkRobotModel.is_del != 1)
        return q.first() if q else None

    def update_unselect_by_rtx(self, rtx_id):
        q = self.session.query(DtalkRobotModel)
        q = q.filter(DtalkRobotModel.rtx_id == rtx_id)
        q = q.filter(DtalkRobotModel.is_del != 1)
        q = q.update({DtalkRobotModel.select: False}, synchronize_session=False)
        return q

    def batch_delete_by_md5(self, params):
        if not params.get('list'):
            return 0

        md5_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(DtalkRobotModel)
        q = q.filter(DtalkRobotModel.md5_id.in_(md5_list))
        if rtx_id:
            q = q.filter(DtalkRobotModel.rtx_id == rtx_id)
        q = q.filter(DtalkRobotModel.is_del != 1)
        q = q.update({DtalkRobotModel.is_del: True,
                      DtalkRobotModel.delete_rtx: rtx_id,
                      DtalkRobotModel.delete_time: get_now()},
                     synchronize_session=False)
        return q

    def get_model_by_rtx(self, rtx):
        q = self.session.query(DtalkRobotModel)
        q = q.filter(DtalkRobotModel.rtx_id == str(rtx))
        q = q.filter(DtalkRobotModel.is_del != 1)
        return q.all()

    def get_model_by_key_rtx(self, key, rtx):
        q = self.session.query(DtalkRobotModel)
        q = q.filter(DtalkRobotModel.rtx_id == str(rtx))
        q = q.filter(DtalkRobotModel.key == str(key))
        q = q.filter(DtalkRobotModel.is_del != 1)
        return q.first()

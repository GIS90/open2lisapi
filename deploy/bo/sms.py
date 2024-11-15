# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    sms bo
    
base_info:
    __author__ = "PyGo"
    __time__ = "2024/11/15 22:20"
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
# usage: /usr/bin/python sms.py
# ------------------------------------------------------------
from sqlalchemy import or_

from deploy.utils.utils import get_now
from deploy.bo.bo_base import BOBase
from deploy.model.sms import SmsModel
from deploy.model.enum import EnumModel


class SmsBo(BOBase):

    def __init__(self):
        super(SmsBo, self).__init__()

    def __str__(self):
        return "SmsBo Bo."

    def __repr__(self):
        return self.__str__()

    def new_mode(self):
        return SmsModel()

    def get_all(self, params: dict):
        q = self.session.query(SmsModel)
        q = q.filter(SmsModel.is_del != 1)
        if params.get('rtx_id'):
            q = q.filter(SmsModel.rtx_id == str(params.get('rtx_id')))
        # 选择下载条件
        if params.get('list'):
            q = q.filter(SmsModel.md5_id.in_(params.get('list')))
        q = q.order_by(SmsModel.create_time.desc())
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

    def get_model_by_md5(self, md5):
        q = self.session.query(SmsModel)
        q = q.filter(SmsModel.md5_id == str(md5))
        return q.first() if q else None

    def batch_delete_by_md5(self, params):
        if not params.get('list'):
            return 0

        md5_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(SmsModel)
        q = q.filter(SmsModel.md5_id.in_(md5_list))
        if rtx_id:
            q = q.filter(SmsModel.rtx_id == rtx_id)
        q = q.filter(SmsModel.is_del != 1)
        q = q.update({SmsModel.is_del: True,
                      SmsModel.delete_rtx: rtx_id,
                      SmsModel.delete_time: get_now()},
                     synchronize_session=False)
        return q

# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    DtalkMessage Bo

base_info:
    __author__ = "PyGo"
    __time__ = "2022/7/18 21:22"
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
# usage: /usr/bin/python dtalk_message.py
# ------------------------------------------------------------
from sqlalchemy import or_

from deploy.utils.utils import get_now
from deploy.bo.bo_base import BOBase
from deploy.model.dtalk_message import DtalkMessageModel


class DtalkMessageBo(BOBase):

    def __init__(self):
        super(DtalkMessageBo, self).__init__()

    def __str__(self):
        return "DtalkMessage Bo."

    def __repr__(self):
        return self.__str__()

    def new_mode(self):
        return DtalkMessageModel()

    def get_all(self, params: dict):
        q = self.session.query(DtalkMessageModel)
        q = q.filter(DtalkMessageModel.is_del != 1)
        if params.get('rtx_id'):
            q = q.filter(DtalkMessageModel.rtx_id == str(params.get('rtx_id')))
        q = q.order_by(DtalkMessageModel.create_time.desc())
        # 选择下载条件
        if params.get('list'):
            q = q.filter(DtalkMessageModel.md5_id.in_(params.get('list')))
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

    def get_model_by_md5(self, md5):
        q = self.session.query(DtalkMessageModel)
        q = q.filter(DtalkMessageModel.md5_id == str(md5))
        return q.first() if q else None

    def batch_delete_by_md5(self, params):
        if not params.get('list'):
            return 0

        md5_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(DtalkMessageModel)
        q = q.filter(DtalkMessageModel.md5_id.in_(md5_list))
        if rtx_id:
            q = q.filter(DtalkMessageModel.rtx_id == rtx_id)
        q = q.filter(DtalkMessageModel.is_del != 1)
        q = q.update({DtalkMessageModel.is_del: True,
                      DtalkMessageModel.delete_rtx: rtx_id,
                      DtalkMessageModel.delete_time: get_now()},
                     synchronize_session=False)
        return q

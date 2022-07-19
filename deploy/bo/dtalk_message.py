# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

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

from deploy.bo.bo_base import BOBase
from deploy.models.dtalk_message import DtalkMessageModel


class DtalkMessageBo(BOBase):

    def __init__(self):
        super(DtalkMessageBo, self).__init__()

    def new_mode(self):
        return DtalkMessageModel()

    def get_all(self, params: dict):
        q = self.session.query(DtalkMessageModel)
        q = q.filter(DtalkMessageModel.is_del != 1)
        if params.get('rtx_id'):
            q = q.filter(DtalkMessageModel.rtx_id == str(params.get('rtx_id')))
        q = q.order_by(DtalkMessageModel.create_time.desc())
        if not q:
            return [], 0
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

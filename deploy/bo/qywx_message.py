# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    QywxMessage Bo

base_info:
    __author__ = "PyGo"
    __time__ = "2022/11/9 21:35"
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
# usage: /usr/bin/python qywx_message.py
# ------------------------------------------------------------
from sqlalchemy import or_

from deploy.utils.utils import get_now
from deploy.bo.bo_base import BOBase
from deploy.model.qywx_message import QywxMessageModel
from deploy.model.enum import EnumModel


class QywxMessageBo(BOBase):

    def __init__(self):
        super(QywxMessageBo, self).__init__()

    def __str__(self):
        return "QywxMessage Bo."

    def __repr__(self):
        return self.__str__()

    def new_mode(self):
        return QywxMessageModel()

    def get_all(self, params: dict):
        q = self.session.query(QywxMessageModel.id,
                               QywxMessageModel.rtx_id,
                               QywxMessageModel.title,
                               QywxMessageModel.content,
                               QywxMessageModel.user,
                               QywxMessageModel.type,
                               QywxMessageModel.md5_id,
                               QywxMessageModel.robot,
                               QywxMessageModel.count,
                               QywxMessageModel.last_send_time,
                               QywxMessageModel.create_time,
                               QywxMessageModel.delete_rtx,
                               QywxMessageModel.delete_time,
                               QywxMessageModel.is_del,
                               QywxMessageModel.is_back,
                               QywxMessageModel.msg_id,
                               EnumModel.name.label('enum_name'),
                               EnumModel.key.label('enum_key'),
                               EnumModel.value.label('enum_value'))
        q = q.filter(QywxMessageModel.type == EnumModel.key)
        q = q.filter(QywxMessageModel.is_del != 1)
        if params.get('enum_name'):
            q = q.filter(EnumModel.name == str(params.get('enum_name')).lower())
        if params.get('rtx_id'):
            q = q.filter(QywxMessageModel.rtx_id == str(params.get('rtx_id')))
        q = q.order_by(QywxMessageModel.create_time.desc())
        if not q:
            return [], 0
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

    def get_model_by_md5(self, md5):
        q = self.session.query(QywxMessageModel)
        q = q.filter(QywxMessageModel.md5_id == str(md5))
        return q.first() if q else None

    def batch_delete_by_md5(self, params):
        if not params.get('list'):
            return 0

        md5_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(QywxMessageModel)
        q = q.filter(QywxMessageModel.md5_id.in_(md5_list))
        if rtx_id:
            q = q.filter(QywxMessageModel.rtx_id == rtx_id)
        q = q.filter(QywxMessageModel.is_del != 1)
        q = q.update({QywxMessageModel.is_del: True,
                      QywxMessageModel.delete_rtx: rtx_id,
                      QywxMessageModel.delete_time: get_now()},
                     synchronize_session=False)
        return q

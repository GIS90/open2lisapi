# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    model class              DB table
    ---------------------------------------
    QywxMessageModel         qywx_message

base_info:
    __author__ = "PyGo"
    __time__ = "2022/11/09 21:33"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    from deploy.model.qywx_message import QywxMessageModel

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
from sqlalchemy import (
        Column,
        String,
        Integer,
        Boolean,
        TIMESTAMP,
        Text
)
from deploy.model import base


__all__ = ["QywxMessageModel"]


class QywxMessageModel(base.ModelBase):
    __tablename__ = 'qywx_message'

    id = Column(Integer, primary_key=True)
    rtx_id = Column(String(25))
    title = Column(String(55))
    content = Column(Text)
    user = Column(Text)
    type = Column(String(55))
    md5_id = Column(String(55))
    msg_id = Column(String(64))
    robot = Column(String(55))
    count = Column(Integer)
    last_send_time = Column(TIMESTAMP)
    create_time = Column(TIMESTAMP)
    delete_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP)
    is_del = Column(Boolean())
    is_back = Column(Boolean())

    def __str__(self):
        return "QywxMessageModel Class, relate to DB table: qywx_message."

    def __repr__(self):
        return self.__str__()

# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    sms model

base_info:
    __author__ = "PyGo"
    __time__ = "2024/11/13 22:26"
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
from sqlalchemy import (
        Column,
        Integer,
        SmallInteger,
        String,
        Float,
        DECIMAL,
        Boolean,
        Date,
        DateTime,
        Time,
        TIMESTAMP,
        Enum,
        Text
)

from sqlalchemy import func
from deploy.model import base


__all__ = ["SmsModel"]


class SmsModel(base.ModelBase):
    __tablename__ = 'sms_model'

    id = Column(Integer, primary_key=True)
    rtx_id = Column(String(25))
    md5_id = Column(String(55))
    telephone = Column(String(2000))
    content = Column(String(255))
    mass = Column(Boolean())
    send = Column(Boolean())
    success = Column(String(2000))
    failure = Column(String(2000))
    create_time = Column(TIMESTAMP())
    update_rtx = Column(String(25))
    update_time = Column(TIMESTAMP())
    delete_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP())
    is_del = Column(Boolean())

    # 定义DB默认操作[过时]
    # __mapper_args = {"order_by": id}

    def __str__(self):
        return "SmsModel Class, relate to DB table: sms."

    def __repr__(self):
        return self.__str__()

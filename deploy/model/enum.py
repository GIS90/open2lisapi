# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    enum

base_info:
    __author__ = "PyGo"
    __time__ = "2022/4/27 2:44 下午"
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
# usage: /usr/bin/python enum.py
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


__all__ = ("EnumModel")


class EnumModel(base.ModelBase):
    __tablename__ = 'enum'

    id = Column(Integer, primary_key=True)
    name = Column(String(35))
    md5_id = Column(String(55))
    key = Column(String(55))
    value = Column(String(55))
    description = Column(Text)
    status = Column(Boolean())
    create_rtx = Column(String(25))
    create_time = Column(TIMESTAMP)
    update_rtx = Column(String(25))
    update_time = Column(TIMESTAMP)
    delete_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP)
    is_del = Column(Boolean())
    order_id = Column(Integer)
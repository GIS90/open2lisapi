# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    dtalk-robot

base_info:
    __author__ = "PyGo"
    __time__ = "2022/7/12 19:29"
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
# usage: /usr/bin/python dtalk_config.py
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


__all__ = ("DtalkRobotModel")


class DtalkRobotModel(base.ModelBase):
    __tablename__ = 'dtalk_robot'

    id = Column(Integer, primary_key=True)
    rtx_id = Column(String(25))
    name = Column(String(30))
    md5_id = Column(String(55))
    key = Column(String(30))
    secret = Column(String(70))
    select = Column(Boolean())
    description = Column(Text)
    create_time = Column(TIMESTAMP)
    delete_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP)
    is_del = Column(Boolean())


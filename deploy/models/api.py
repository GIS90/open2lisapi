# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/3/4 10:45 上午"
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

# ------------------------------------------------------------
# usage: /usr/bin/python api.py
# ------------------------------------------------------------
from sqlalchemy import (
        Column,
        String,
        Integer,
        Boolean,
        TIMESTAMP,
        Text
)
from deploy.models import base


__all__ = ("ApiModel")


class ApiModel(base.ModelBase):
    __tablename__ = 'api'

    id = Column(Integer, primary_key=True)
    blueprint = Column(String(15))
    apiname = Column(String(25))
    endpoint = Column(String(41))
    path = Column(String(45))
    type = Column(String(15))
    short = Column(String(35))
    long = Column(String(120))
    create_time = Column(TIMESTAMP())
    create_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP())
    delete_rtx = Column(String(25))
    is_del = Column(Boolean())
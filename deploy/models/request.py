# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    request

base_info:
    __author__ = "PyGo"
    __time__ = "2022/3/2 10:45 下午"
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
# usage: /usr/bin/python request.py
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


__all__ = ("RequestModel")


class RequestModel(base.ModelBase):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)
    rtx_id = Column(String(25))
    ip = Column(String(15))
    blueprint = Column(String(25))
    endpoint = Column(String(35))
    method = Column(String(10))
    path = Column(String(35))
    full_path = Column(String(85))
    host_url = Column(String(55))
    url = Column(String(120))
    create_time = Column(TIMESTAMP())


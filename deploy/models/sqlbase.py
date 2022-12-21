# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/12/21 20:35"
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
# usage: /usr/bin/python sqlbase.py
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


__all__ = ("SqlbaseModel")


class SqlbaseModel(base.ModelBase):
    __tablename__ = 'sqlbase'

    id = Column(Integer, primary_key=True)
    rtx_id = Column(String(25))
    title = Column(String(55))
    md5_id = Column(String(55))
    author = Column(String(25))
    recommend = Column(Integer)
    summary = Column(String(200))
    label = Column(String(35))
    public = Column(Boolean())
    public_time = Column(TIMESTAMP)
    content = Column(Text)
    create_time = Column(TIMESTAMP)
    delete_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP)
    is_del = Column(Boolean())

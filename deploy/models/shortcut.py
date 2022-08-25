# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    shortcut model

base_info:
    __author__ = "PyGo"
    __time__ = "2022/8/25 21:39"
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
# usage: /usr/bin/python shortcut.py
# ------------------------------------------------------------
from sqlalchemy import (
        Column,
        String,
        Integer,
        Boolean,
        TIMESTAMP,
        Text,
        DateTime
)
from deploy.models import base


__all__ = ("ShortCutModel")


class ShortCutModel(base.ModelBase):
    __tablename__ = 'shortcut'

    id = Column(Integer, primary_key=True)
    rtx_id = Column(String(25))
    shortcut = Column(String(120))
    create_time = Column(TIMESTAMP)
    update_rtx = Column(String(25))
    update_time = Column(DateTime)
    is_del = Column(Boolean())


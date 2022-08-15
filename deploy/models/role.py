# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    role

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/20 9:25 上午"
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
# usage: /usr/bin/python role.py
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


__all__ = ("RoleModel")


class RoleModel(base.ModelBase):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    engname = Column(String(25))
    chnname = Column(String(35))
    md5_id = Column(String(55))
    authority = Column(String(120))
    introduction = Column(Text)
    create_time = Column(TIMESTAMP())
    create_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP())
    delete_rtx = Column(String(25))
    is_del = Column(Boolean())

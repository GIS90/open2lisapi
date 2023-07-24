# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    sysuser_avatar model
base_info:
    __author__ = "PyGo"
    __time__ = "2023/7/24 07:13"
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
# usage: /usr/bin/python sysuser_avatar.py
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


__all__ = ("SysUserAvatarModel")


class SysUserAvatarModel(base.ModelBase):
    __tablename__ = 'sysuser_avatar'

    id = Column(Integer, primary_key=True)
    rtx_id = Column(String(25))
    md5_id = Column(String(55))
    name = Column(String(55))
    summary = Column(String(200))
    label = Column(String(35))
    url = Column(String(120))
    count = Column(Integer)
    create_time = Column(TIMESTAMP())
    update_rtx = Column(String(25))
    update_time = Column(TIMESTAMP())
    delete_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP())
    is_del = Column(Boolean())
    order_id = Column(Integer)



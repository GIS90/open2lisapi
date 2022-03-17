# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    sysuser table

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
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
from sqlalchemy import (
        Column,
        String,
        Integer,
        Boolean,
        TIMESTAMP,
        Text
)
from deploy.models import base


__all__ = ("SysUserModel")


class SysUserModel(base.ModelBase):
    __tablename__ = 'sysuser'

    id = Column(Integer, primary_key=True)
    rtx_id = Column(String(25))
    md5_id = Column(String(55))
    fullname = Column(String(30))
    password = Column(String(30))
    email = Column(String(25))
    phone = Column(String(15))
    avatar = Column(String(255))
    introduction = Column(Text)
    department = Column(String(55))
    role = Column(String(55))
    create_time = Column(TIMESTAMP())
    create_operator = Column(String(25))
    is_del = Column(Boolean())
    del_time = Column(TIMESTAMP())
    del_operator = Column(String(25))


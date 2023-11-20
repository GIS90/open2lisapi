# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table
    ---------------------------------------
    ShortCutModel            shortcut

base_info:
    __author__ = "PyGo"
    __time__ = "2022/8/25 21:39"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    from deploy.model.shortcut import ShortCutModel

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
from deploy.model import base


__all__ = ["ShortCutModel"]


class ShortCutModel(base.ModelBase):
    __tablename__ = 'shortcut'

    id = Column(name="id", type_=Integer,  autoincrement="auto", primary_key=True, comment="主键，自增ID")
    rtx_id = Column(name="rtx_id", type_=String(25), nullable=False, comment="用户RTX-ID")
    shortcut = Column(name="shortcut", type_=String(120), comment="角色权限ID集合，用英文；分割")
    create_time = Column(name="create_time", type_=TIMESTAMP, nullable=False, comment="创建时间")
    update_rtx = Column(name="update_rtx", type_=String(25), comment="最新更新操作人")
    update_time = Column(name="update_time", type_=DateTime, comment="最新更新时间")
    is_del = Column(name="is_del", type_=Boolean(), default=False, comment="是否删除标识")

    def __str__(self):
        return "ShortCutModel Class, relate to DB table: shortcut."

    def __repr__(self):
        return self.__str__()

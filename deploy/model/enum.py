# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table
    ---------------------------------------
    EnumModel                enum

base_info:
    __author__ = "PyGo"
    __time__ = "2022/4/27 2:44 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    from deploy.model.enum import EnumModel

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


__all__ = ["EnumModel"]


class EnumModel(base.ModelBase):
    __tablename__ = 'enum'

    id = Column(name="id", type_=Integer,  autoincrement="auto", primary_key=True, comment="主键，自增ID")
    name = Column(name="name", type_=String(35), nullable=False, comment="枚举名称")
    md5_id = Column(name="md5_id", type_=String(55), nullable=False, comment="唯一标识：MD5-ID")
    key = Column(name="key", type_=String(55), nullable=False, comment="枚举子集对应的key")
    value = Column(name="value", type_=String(55), nullable=False, comment="枚举子集对应的value")
    description = Column(name="description", type_=Text, comment="枚举子集对应的value说明")
    status = Column(name="status", type_=Boolean(), comment="状态")
    create_time = Column(name="create_time", type_=TIMESTAMP, nullable=False, comment="创建时间")
    create_rtx = Column(name="create_rtx", type_=String(25), nullable=False, comment="创建用户")
    update_time = Column(name="update_time", type_=TIMESTAMP, comment="最新更新时间")
    update_rtx = Column(name="update_rtx", type_=String(25), comment="最新更新用户")
    delete_time = Column(name="delete_time", type_=TIMESTAMP, comment="删除时间")
    delete_rtx = Column(name="delete_rtx", type_=String(25), comment="删除用户")
    is_del = Column(name="is_del", type_=Boolean(), default=False, comment="是否删除标识")
    order_id = Column(name="order_id", type_=Integer, comment="排序ID")

    def __str__(self):
        return "EnumModel Class, relate to DB table: enum."

    def __repr__(self):
        return self.__str__()


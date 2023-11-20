# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table
    ---------------------------------------
    RoleModel                role

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/20 9:25 上午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    from deploy.model.role import RoleModel

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
from deploy.model import base


__all__ = ["RoleModel"]


class RoleModel(base.ModelBase):
    __tablename__ = 'role'

    id = Column(name="id", type_=Integer, primary_key=True, comment="主键，自增ID")
    engname = Column(name="engname", type_=String(25), nullable=False, unique=True, comment="角色英文名称，唯一值")
    chnname = Column(name="chnname", type_=String(35), nullable=False, comment="角色中文名称")
    md5_id = Column(name="md5_id", type_=String(55), nullable=False, comment="唯一标识：MD5-ID")
    authority = Column(name="authority", type_=String(120), comment="角色权限ID集合，用英文；分割")
    introduction = Column(name="introduction", type_=Text, comment="角色描述")
    create_time = Column(name="create_time", type_=TIMESTAMP(), nullable=False, comment="创建时间")
    create_rtx = Column(name="create_rtx", type_=String(25), nullable=False, comment="创建用户")
    delete_time = Column(name="delete_time", type_=TIMESTAMP(), comment="删除时间")
    delete_rtx = Column(name="delete_rtx", type_=String(25), comment="删除用户")
    is_del = Column(name="is_del", type_=Boolean(), default=False, comment="是否删除标识")

    def __str__(self):
        return "RoleModel Class, relate to DB table: role."

    def __repr__(self):
        return self.__str__()


# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table
    ---------------------------------------
    ApiModel                 api

base_info:
    __author__ = "PyGo"
    __time__ = "2022/3/4 10:45 上午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    from deploy.model.api import ApiModel

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
from deploy.model import base


__all__ = ["ApiModel"]


class ApiModel(base.ModelBase):
    __tablename__ = 'api'

    id = Column(name="id", type_=Integer,  autoincrement="auto", primary_key=True, comment="主键，自增ID")
    blueprint = Column(name="blueprint", type_=String(15), nullable=False, comment="API接口blueprint")
    apiname = Column(name="apiname", type_=String(35), nullable=False, comment="API接口View方法名称")
    endpoint = Column(name="endpoint", type_=String(55), nullable=False, comment="API接口endpoint")
    md5_id = Column(name="md5_id", type_=String(55), nullable=False, comment="唯一标识：MD5-ID")
    path = Column(name="path", type_=String(55), nullable=False, comment="API接口path，与request表关联")
    type = Column(name="type", type_=String(15), default="success", comment="API接口类型：primary登录/success数据获取/warning/danger退出/info新增/更新/删除数据")
    short = Column(name="short", type_=String(35), comment="API接口简述")
    long = Column(name="long", type_=String(120), comment="API接口详细描述")
    create_time = Column(name="create_time", type_=TIMESTAMP(), nullable=False, comment="创建时间")
    create_rtx = Column(name="create_rtx", type_=String(25), nullable=False, comment="创建操作人")
    delete_time = Column(name="delete_time", type_=TIMESTAMP(), comment="删除时间")
    delete_rtx = Column(name="delete_rtx", type_=String(25), comment="删除操作人")
    update_time = Column(name="update_time", type_=TIMESTAMP(), comment="最近修改时间")
    update_rtx = Column(name="update_rtx", type_=String(25), comment="最近修改操作人")
    is_del = Column(name="is_del", type_=Boolean(), comment="是否删除标识")
    order_id = Column(name="order_id", type_=Integer, comment="顺序ID")

    def __str__(self):
        return "ApiModel Class, relate to DB table: api."

    def __repr__(self):
        return self.__str__()


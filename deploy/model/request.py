# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table
    ---------------------------------------
    RequestModel             request

base_info:
    __author__ = "PyGo"
    __time__ = "2022/3/2 10:45 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    from deploy.model.request import RequestModel

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
        Text,
        Date,
        DECIMAL
)
from deploy.model import base


__all__ = ["RequestModel"]


class RequestModel(base.ModelBase):
    __tablename__ = 'request'

    id = Column(name="id", type_=Integer,  autoincrement="auto", primary_key=True, comment="主键，自增ID")
    rtx_id = Column(name="rtx_id", type_=String(25), nullable=False, comment="请求访问用户rtx-id唯一标识")
    ip = Column(name="ip", type_=String(15), comment="用户IP")
    blueprint = Column(name="blueprint", type_=String(15), comment="API地址blueprint")
    apiname = Column(name="apiname", type_=String(25), comment="API接口View方法名称")
    endpoint = Column(name="endpoint", type_=String(41), comment="API地址endpoint")
    method = Column(name="method", type_=String(10), comment="API请求method")
    path = Column(name="path", type_=String(45), comment="API请求path")
    full_path = Column(name="full_path", type_=String(85), comment="API地址full_path")
    host_url = Column(name="host_url", type_=String(55), comment="API地址host_url")
    url = Column(name="url", type_=String(120), comment="API地址url")
    cost = Column(name="cost", type_=DECIMAL(10, 4), comment="API运行时间")
    create_time = Column(name="create_time", type_=TIMESTAMP(), nullable=False, comment="创建时间")
    create_date = Column(name="create_date", type_=Date(), nullable=False, comment="创建日期")

    def __str__(self):
        return "RequestModel Class, relate to DB table: request."

    def __repr__(self):
        return self.__str__()

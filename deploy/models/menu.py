# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    menu

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/22 11:09 上午"
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
# usage: /usr/bin/python menu.py
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


__all__ = ("MenuModel")


class MenuModel(base.ModelBase):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    path = Column(String(35))
    title = Column(String(25))
    pid = Column(Integer)
    level = Column(Integer)
    md5_id = Column(String(55))
    component = Column(String(25))
    hidden = Column(Boolean())
    redirect = Column(String(35))
    icon = Column(String(25))
    cache = Column(Boolean())
    affix = Column(Boolean())
    breadcrumb = Column(Boolean())
    order_id = Column(Integer)
    create_time = Column(TIMESTAMP())
    create_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP())
    delete_rtx = Column(String(25))
    is_del = Column(Boolean())

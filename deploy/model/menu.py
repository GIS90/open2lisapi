# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table
    ---------------------------------------
    MenuModel                menu

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/22 11:09 上午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    from deploy.model.menu import MenuModel

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
from deploy.model import base


__all__ = ["MenuModel"]


class MenuModel(base.ModelBase):
    __tablename__ = 'menu'

    id = Column(name="id", type_=Integer,  autoincrement="auto", primary_key=True, comment="主键，自增ID")
    name = Column(name="name", type_=String(25), nullable=False, comment="路由rtx-id，大驼峰命名方式")
    path = Column(name="path", type_=String(35), nullable=False, comment="路由path，全小写字母")
    title = Column(name="title", type_=String(25), nullable=False, comment="菜单名称")
    pid = Column(name="pid", type_=Integer, nullable=False, comment="父ID")
    level = Column(name="level", type_=Integer, nullable=False, comment="菜单级别")
    md5_id = Column(name="md5_id", type_=String(55), nullable=False, comment="唯一标识：MD5-ID")
    component = Column(name="component", type_=String(25), nullable=False, comment="路由组件，与Vue router mappings映射")
    hidden = Column(name="hidden", type_=Boolean(), comment="是否在SideBar显示，默认为false")
    redirect = Column(name="redirect", type_=String(35), comment="菜单重定向，主要用于URL一级菜单跳转")
    icon = Column(name="icon", type_=String(25), comment="菜单图标")
    cache = Column(name="cache", type_=Boolean(), comment="页面是否进行cache，默认true缓存")
    affix = Column(name="affix", type_=Boolean(), comment="是否在tags-view固定，默认false")
    breadcrumb = Column(name="breadcrumb", type_=Boolean(), comment="是否breadcrumb中显示，默认true")
    order_id = Column(name="order_id", type_=Integer, comment="排序ID")
    create_time = Column(name="create_time", type_=TIMESTAMP(), nullable=False, comment="创建时间")
    create_rtx = Column(name="create_rtx", type_=String(25), nullable=False, comment="创建操作人")
    delete_time = Column(name="delete_time", type_=TIMESTAMP(), comment="删除时间")
    delete_rtx = Column(name="delete_rtx", type_=String(25), comment="删除操作人")
    is_del = Column(name="is_del", type_=Boolean(), default=False, comment="是否删除标识")
    is_shortcut = Column(name="is_shortcut", type_=Boolean(), default=True, comment="Dashboard快捷入口是否显示")

    def __str__(self):
        return "MenuModel Class, relate to DB table: menu."

    def __repr__(self):
        return self.__str__()


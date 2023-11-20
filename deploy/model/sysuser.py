# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    Python                   DB
    ---------------------------------------
    SysUserModel             sysuser

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "twtoolbox_isapi"

usage:
    from deploy.model.sysuser import SysUserModel

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
from deploy.model import base


__all__ = ("SysUserModel")


class SysUserModel(base.ModelBase):
    __tablename__ = 'sysuser'

    id = Column(name="id", type_=Integer,  autoincrement="auto", primary_key=True, comment="主键，自增ID")
    rtx_id = Column(name="rtx_id", type_=String(25), nullable=False, comment="用户rtx-id唯一标识")
    md5_id = Column(name="md5_id", type_=String(55), nullable=False, comment="用户rtx-md5-id唯一数据标识")
    fullname = Column(name="fullname", type_=String(30), nullable=False, comment="用户名称")
    password = Column(name="password", type_=String(30), nullable=False, comment="用户明文密码")
    email = Column(name="email", type_=String(35), comment="用户邮箱")
    phone = Column(name="phone", type_=String(15), comment="用户电话")
    avatar = Column(name="avatar", type_=String(120), comment="用户头像地址")
    introduction = Column(name="introduction", type_=Text, comment="用户描述")
    role = Column(name="role", type_=String(80), nullable=False, comment="用户角色engname值，关联role表，多角色用;分割")
    department = Column(name="department", type_=String(55), comment="用户部门md5-id值，关联department表")
    create_time = Column(name="create_time", type_=TIMESTAMP(), nullable=False, comment="创建时间")
    create_rtx = Column(name="create_rtx", type_=String(25), nullable=False, comment="创建操作人")
    delete_time = Column(name="delete_time", type_=TIMESTAMP(), comment="删除时间")
    delete_rtx = Column(name="delete_rtx", type_=String(25), comment="删除操作人")
    is_del = Column(name="is_del", type_=Boolean(), default=False, comment="是否删除状态：True删除；False未删除")

    def __str__(self):
        return "SysUserModel Class, relate to DB table: sysuser."

    def __repr__(self):
        return self.__str__()

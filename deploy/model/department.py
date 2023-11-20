# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table
    ---------------------------------------
    DepartmentModel          department

base_info:
    __author__ = "PyGo"
    __time__ = "2022/10/9 23:59"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    from deploy.model.department import DepartmentModel

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python department.py
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


__all__ = ["DepartmentModel"]


class DepartmentModel(base.ModelBase):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    md5_id = Column(String(55))
    description = Column(Text)
    pid = Column(Integer)
    leaf = Column(Boolean())
    lock = Column(Boolean())
    dept_path = Column(String(254))
    deptid_path = Column(String(254))
    manage_rtx = Column(String(25))
    create_time = Column(TIMESTAMP())
    create_rtx = Column(String(25))
    update_time = Column(TIMESTAMP())
    update_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP())
    delete_rtx = Column(String(25))
    is_del = Column(Boolean())
    order_id = Column(Integer)

    def __str__(self):
        return "DepartmentModel Class, relate to DB table: department."

    def __repr__(self):
        return self.__str__()


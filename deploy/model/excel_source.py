# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table
    ---------------------------------------
    ExcelSourceModel         excel_source

base_info:
    __author__ = "PyGo"
    __time__ = "2022/3/29 10:57 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    from deploy.model.excel_source import ExcelSourceModel

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python excel_source.py
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


__all__ = ["ExcelSourceModel"]


class ExcelSourceModel(base.ModelBase):
    __tablename__ = 'excel_source'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    store_name = Column(String(100))
    md5_id = Column(String(55))
    rtx_id = Column(String(25))
    ftype = Column(String(2))
    local_url = Column(String(120))
    store_url = Column(String(120))
    numopr = Column(Integer)
    nsheet = Column(Integer)
    set_sheet = Column(String(35))
    sheet_names = Column(Text)
    sheet_columns = Column(Text)
    headers = Column(Text)
    create_time = Column(TIMESTAMP)
    delete_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP)
    is_del = Column(Boolean())

    def __str__(self):
        return "ExcelSourceModel Class, relate to DB table: excel_source."

    def __repr__(self):
        return self.__str__()
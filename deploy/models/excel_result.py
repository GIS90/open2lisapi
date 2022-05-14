# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/3/29 10:57 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

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
# usage: /usr/bin/python excel_result.py
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


__all__ = ("ExcelResultModel")


class ExcelResultModel(base.ModelBase):
    __tablename__ = 'excel_result'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    store_name = Column(String(100))
    md5_id = Column(String(55))
    ftype = Column(String(2))
    rtx_id = Column(String(25))
    local_url = Column(String(120))
    store_url = Column(String(120))
    is_compress = Column(Boolean())
    nfile = Column(Integer)
    nsheet = Column(Integer)
    row = Column(Integer)
    col = Column(Integer)
    sheet_names = Column(Text)
    sheet_columns = Column(Text)
    headers = Column(Text)
    create_time = Column(TIMESTAMP)
    delete_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP)
    is_del = Column(Boolean())

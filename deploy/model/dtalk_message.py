# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    model class              DB table
    ---------------------------------------
    DtalkMessageModel        dtalk_message

base_info:
    __author__ = "PyGo"
    __time__ = "2022/7/12 19:29"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:
    from deploy.model.dtalk_message import DtalkMessageModel

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python dtalk_message.py
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


__all__ = ["DtalkMessageModel"]


class DtalkMessageModel(base.ModelBase):
    __tablename__ = 'dtalk_message'

    id = Column(Integer, primary_key=True)
    rtx_id = Column(String(25))
    file_name = Column(String(80))
    file_local_url = Column(String(120))
    file_store_url = Column(String(120))
    md5_id = Column(String(55))
    robot = Column(String(55))
    count = Column(Integer)
    number = Column(Integer)
    nsheet = Column(Integer)
    sheet_names = Column(Text)
    sheet_columns = Column(Text)
    headers = Column(Text)
    set_sheet = Column(String(35))
    cur_sheet = Column(String(3))
    set_column = Column(Text)
    set_title = Column(Text)
    create_time = Column(TIMESTAMP)
    delete_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP)
    is_del = Column(Boolean())

    def __str__(self):
        return "DtalkMessageModel Class, relate to DB table: dtalk_message."

    def __repr__(self):
        return self.__str__()


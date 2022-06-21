# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    office pdf model

base_info:
    __author__ = "PyGo"
    __time__ = "2022/6/8 20:15"
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
# usage: /usr/bin/python office.py
# ------------------------------------------------------------

from sqlalchemy import (
        Column,
        String,
        Integer,
        Boolean,
        TIMESTAMP
)
from deploy.models import base


__all__ = ("OfficePDFModel")


class OfficePDFModel(base.ModelBase):
    __tablename__ = 'office_pdf'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    store_name = Column(String(100))
    transfer_name = Column(String(100))
    md5_id = Column(String(55))
    rtx_id = Column(String(25))
    file_type = Column(String(2))
    transfer = Column(Boolean())
    transfer_time = Column(TIMESTAMP)
    local_url = Column(String(120))
    store_url = Column(String(120))
    transfer_url = Column(String(120))
    mode = Column(Boolean())
    start = Column(Integer)
    end = Column(Integer)
    pages = Column(String(100))
    create_time = Column(TIMESTAMP)
    delete_rtx = Column(String(25))
    delete_time = Column(TIMESTAMP)
    is_del = Column(Boolean())


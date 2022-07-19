# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/5/6 18:53"
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
# usage: /usr/bin/python enums.py
# ------------------------------------------------------------
from enum import Enum


# Excel拆分枚举
EXCEL_SPLIT_STORE = ['1', '2']
# 行列
EXCEL_NUM = ['1', '2']
# bool枚举
BOOL = ['0', '1']


class FileTypeEnum(Enum):
    EXCEL_MERGE = 1
    EXCEL_SPLIT = 2
    WORD = 3
    PPT = 4
    TEXT = 5
    PDF = 6
    DTALK = 7
    OTHER = 99


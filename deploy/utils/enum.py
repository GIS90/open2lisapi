# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    枚举
    存储项目用到的固定值，以Enum枚举的方式对外暴露使用

base_info:
    __author__ = "PyGo"
    __time__ = "2022/9/14"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __project__ = "open2lisapi"

usage:
    from deploy.utils.enums import FileTypeEnum

    for pr in FileTypeEnum:
        if not pr: continue
        LOG.info('%s >>> %s' % (pr.name, pr.value))

design:
    项目常量

reference urls:

python version:
    python3


Enjoy the good time everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python enums.py
# ------------------------------------------------------------
from enum import Enum, unique


# Excel拆分枚举
EXCEL_SPLIT_STORE = ['1', '2']
# 行列
EXCEL_NUM = ['1', '2']
# bool枚举
BOOL = ['0', '1']


# ==============================
# 文件类型
# ==============================
@unique
class FileTypeEnum(Enum):
    EXCEL_MERGE = 1
    EXCEL_SPLIT = 2
    WORD = 3
    PPT = 4
    TEXT = 5
    PDF = 6
    DTALK = 7
    AVATAR = 8
    AVATAR_CROP = 9
    OTHER = 99


# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    创建用户随机头像，用于初始化、个人设置等

base_info:
    __author__ = "PyGo"
    __time__ = "2022/5/19 00:22"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:

design:
    类别设计：
        - 二次元
        - 游戏
        - 美食
        - 宇宙
        - 风景
        - 影视
        - 艺术
        - 时尚
        - 植物
        - 动物
reference urls:

python version:
    python3

store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)
Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python random_avatar.py
# ------------------------------------------------------------
import os

from deploy.config import USER_AVATAR_STORE_URL, USER_AVATAR_STORE_NAME


def _get_store_url():
    return os.path.join(USER_AVATAR_STORE_URL, USER_AVATAR_STORE_NAME)


def get_random_avatar():
    pass


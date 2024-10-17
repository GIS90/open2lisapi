# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    exception

base_info:
    __author__ = "PyGo"
    __time__ = "2023/11/17 15:16"
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
# usage: /usr/bin/python exception.py
# ------------------------------------------------------------


__all__ = ["JwtCredentialsException"]


class JwtCredentialsException(Exception):
    """
    jwt验证异常类
    """
    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return "JwtCredentialsException Class."

    def __repr__(self):
        return self.__str__()

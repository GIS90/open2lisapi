#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    the client of foo
    
    use to run the separate tasks

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
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
--------------------------------------------------------------
"""


# ------------------------------------------------------------
# usage: /usr/bin/python foo.py
# ------------------------------------------------------------
from deploy.utils.base_class import AppBaseClass


class Foo(AppBaseClass):
    def __init__(self):
        super(AppBaseClass, self).__init__()

    def __str__(self):
        return "Foo command."

    def __repr__(self):
        return self.__str__()

    def run(self):
        print("run - " * 10)

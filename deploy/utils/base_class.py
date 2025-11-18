#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    singleton class
    execute base class

base_info:
    __author__ = "PyGo"
    __time__ = "2022/9/14"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __project__ = "open2lisapi"

usage:
    AAAAAClass(WebBaseClass)
    BBBBBClass(AppBaseClass)
    DDDDDClass(Singleton)

design:
    模式设计之一

reference urls:

python version:
    python3


Enjoy the good time everyday！！!
Life is short, I use python.

------------------------------------------------
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python base_class.py
# ------------------------------------------------------------
import threading
from abc import ABC, abstractmethod


class WebBaseClass(ABC):
    """单例模式+ABC"""
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        super(WebBaseClass, self).__init__()
        self.entry_point()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with WebBaseClass._instance_lock:
                cls._instance = object.__new__(cls)
        return cls._instance

    @abstractmethod
    def entry_point(self):
        pass


class Singleton(object):
    """单例模式"""
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        super(Singleton, self).__init__()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with Singleton._instance_lock:
                cls._instance = object.__new__(cls)
        return cls._instance

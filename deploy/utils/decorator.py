# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    Decorator

base_info:
    __author__ = "PyGo"
    __time__ = "2023/11/1 20:58"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "open2lisapi"

usage:

    @deprecated
    @timer
    @debug
    def add(a, b, *args, **kwargs):
        for i in range(10):
            print(i)

    add(100, 300, 1000, c=2000, d=2000)

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python decorators.py
# ------------------------------------------------------------
from datetime import datetime
from functools import wraps
import warnings


def decorator(func):
    """
    装饰器模板
    """
    @wraps(func)
    def __wrapper(*args, **kwargs):
        # 额外功能
        result = func(*args, **kwargs)
        # 额外功能
        print("[Decorator] >>>>> %s." % func.__name__)
        return result
    return __wrapper


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
def timer(func):
    """
    方法执行时间装饰器
    """
    @wraps(func)
    def __wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        cost = round((end_time - start_time).microseconds * pow(0.1, 6), 3)
        print("[timer] >>>>> %s cost %s seconds." % (func.__name__, cost))
        return result
    return __wrapper


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
def debug(func):
    """
    debug装饰器
    """
    @wraps(func)
    def __wrapper(*args, **kwargs):
        print('* ' * 55)
        print("[Debugging] >>>>> %s - args: %s, kwargs: %s" % (func.__name__, args, kwargs))
        print('* ' * 55)
        return func(*args, **kwargs)
    return __wrapper


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
def deprecated(func):
    """
    方法过时提示
    """
    @wraps(func)
    def __wrapper(*args, **kwargs):
        warnings.warn("[%s] is deprecated and will be removed in future versions." % func.__name__, DeprecationWarning)
        return func(*args, **kwargs)
    return __wrapper

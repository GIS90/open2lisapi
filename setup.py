#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    setup packages

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "twtoolbox_isapi"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python setup.py.py
# ------------------------------------------------------------
from setuptools import setup


try:
    import multiprocessing
except ImportError:
    pass

setup(
    setup_requires=['pbr'],
    pbr=True,
)


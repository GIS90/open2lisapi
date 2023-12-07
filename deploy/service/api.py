# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    api service

base_info:
    __author__ = "PyGo"
    __time__ = "2023/9/7 21:01"
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
# usage: /usr/bin/python apis.py
# ------------------------------------------------------------
import json
import requests
import datetime


from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum


class ApiService(object):
    """
    api service
    """

    API_KEY = "R4uejriAnLKV8x1IghtNa7gQ"
    SECRET_KEY = "Dm0Y0SRwX4ccL7c9iNsYwwYmkCHXGFGH"

    def __init__(self):
        """
        ApisService class initialize
        """
        super(ApiService, self).__init__()

    def __str__(self):
        print("ApisService class.")

    def __repr__(self):
        self.__str__()

    def api_demo(self, params: dict) -> dict:
        """
        api: demo
        :return: json data
        """
        return Status(
            100,
            StatusEnum.SUCCESS.value,
            StatusMsgs.get(100),
            {"key1": "value1", "key2": "value2", "key3": "value3"}
        ).json()


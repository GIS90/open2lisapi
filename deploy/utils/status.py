# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    the class of response 
    type: json
    to use api
usage:
    Status(
           101,
           'failure',
           u'Server发生错误，获取失败',
           {}
           ).json()

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/1/16"
    __mail__ = "mingliang.gao@163.com"
------------------------------------------------
"""
import json
from deploy.utils.status_msg import StatusMsgs


class Status(object):
    def __init__(self, status_id: int = 100, status: str = "success", msg: str = "成功", data=None):
        if data is None:
            data = {}
        self.status_body = {
            "status_id": status_id,
            "status": status,
            "message": msg if msg else StatusMsgs.get(status_id),
            "data": data,
        }
        self.data = data
        super(Status, self).__init__()

    def json(self):
        return json.dumps(self.status_body)







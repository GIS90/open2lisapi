# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/3/2 10:48 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "twtoolbox_isapi"

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
# usage: /usr/bin/python request.py
# ------------------------------------------------------------
from deploy.bo.bo_base import BOBase
from deploy.models.request import RequestModel
from deploy.models.api import ApiModel


class RequestBo(BOBase):

    def __init__(self):
        super(RequestBo, self).__init__()

    def new_mode(self):
        return RequestModel()

    def get_by_rtx(self, params):
        if not params:
            return []
        q = self.session.query(RequestModel.id,
                               RequestModel.rtx_id,
                               RequestModel.ip,
                               RequestModel.blueprint,
                               RequestModel.endpoint,
                               RequestModel.method,
                               RequestModel.path,
                               RequestModel.full_path,
                               RequestModel.host_url,
                               RequestModel.url,
                               RequestModel.create_time,
                               ApiModel.type,
                               ApiModel.short,
                               ApiModel.long)
        q = q.filter(RequestModel.blueprint == ApiModel.blueprint)
        q = q.filter(RequestModel.endpoint == ApiModel.endpoint)
        # q = q.filter(RequestModel.path == ApiModel.path)
        if params.get('rtx_id'):
            q = q.filter(RequestModel.rtx_id == params.get('rtx_id'))
        q = q.order_by(RequestModel.create_time.desc())
        if not q:
            return [], 0
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        # print(q)
        return q.all(), total

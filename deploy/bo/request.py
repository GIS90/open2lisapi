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
from sqlalchemy import distinct, func

from deploy.bo.bo_base import BOBase
from deploy.models.request import RequestModel
from deploy.models.api import ApiModel


class RequestBo(BOBase):

    def __init__(self):
        super(RequestBo, self).__init__()

    def new_mode(self):
        return RequestModel()

    def execute_sql(self, sql):
        if not sql:
            return None
        q = self.session.execute(sql)
        return q

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
        q = q.filter(RequestModel.apiname == ApiModel.apiname)
        q = q.filter(RequestModel.endpoint == ApiModel.endpoint)
        # q = q.filter(RequestModel.path == ApiModel.path)
        q = q.filter(ApiModel.is_del != 1)
        if params.get('rtx_id'):
            q = q.filter(RequestModel.rtx_id == params.get('rtx_id'))
        q = q.order_by(RequestModel.create_time.desc())
        print(q)
        if not q:
            return [], 0
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

    def get_user_count_by_time(self, params):
        start_time = params.get('start_time')
        end_time = params.get('end_time')
        q = self.session.query(distinct(RequestModel.rtx_id))
        if start_time:
            q = q.filter(RequestModel.create_time >= start_time)
        if end_time:
            q = q.filter(RequestModel.create_time <= end_time)
        return len(q.all())

    def get_req_count_by_time(self, params):
        start_time = params.get('start_time')
        end_time = params.get('end_time')
        q = self.session.query(func.count(1).label('count'))
        if start_time:
            q = q.filter(RequestModel.create_time >= start_time)
        if end_time:
            q = q.filter(RequestModel.create_time <= end_time)
        return q.first()

    def get_req_count_by_week(self, params):
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        # 方式一
        nums = func.count(1).label('count')
        q = self.session.query(RequestModel.create_date, nums).group_by(RequestModel.create_date)
        # 方式二
        # q = self.session.query(RequestModel.create_date, func.count(1).label('count'))
        # .group_by(RequestModel.create_date)
        if start_date:
            q = q.filter(RequestModel.create_date >= start_date)
        if end_date:
            q = q.filter(RequestModel.create_date <= end_date)
        q = q.order_by(RequestModel.create_date.asc())
        return q.all()

    def get_func_rank(self, params):
        start_time = params.get('start_time')
        end_time = params.get('end_time')
        func_names = params.get('func_names')
        q = self.session.query(RequestModel.endpoint, func.count(1).label('count')).\
            group_by(RequestModel.endpoint)
        if start_time:
            q = q.filter(RequestModel.create_time >= start_time)
        if end_time:
            q = q.filter(RequestModel.create_time <= end_time)
        if func_names:
            q = q.filter(RequestModel.endpoint.in_(func_names))
        q = q.order_by(func.count(1).desc())
        return q.all()

    def get_func_rank_group_by_api_date(self, params):
        start_time = params.get('start_time')
        end_time = params.get('end_time')
        func_names = params.get('func_names')
        nums = func.count(1).label('count')
        q = self.session.query(RequestModel.endpoint, RequestModel.create_date, nums)\
            .group_by(RequestModel.endpoint, RequestModel.create_date)
        if start_time:
            q = q.filter(RequestModel.create_time >= start_time)
        if end_time:
            q = q.filter(RequestModel.create_time <= end_time)
        if func_names:
            q = q.filter(RequestModel.endpoint.in_(func_names))
        q = q.order_by(RequestModel.endpoint.asc(), RequestModel.create_date.asc())
        return q.all()

    def get_req_operate_count_by_week(self, params):
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        nums = func.count(1).label('count')
        q = self.session.query(RequestModel.create_date, nums).group_by(RequestModel.create_date)
        q = q.filter(RequestModel.blueprint == ApiModel.blueprint)
        q = q.filter(RequestModel.endpoint == ApiModel.endpoint)
        q = q.filter(ApiModel.type == 'success')
        if start_date:
            q = q.filter(RequestModel.create_date >= start_date)
        if end_date:
            q = q.filter(RequestModel.create_date <= end_date)
        q = q.order_by(RequestModel.create_date.asc())
        return q.all()

    def get_req_operate_by_time(self, params):
        start_time = params.get('start_time')
        end_time = params.get('end_time')
        q = self.session.query(func.count(1).label('count'))
        q = q.filter(RequestModel.blueprint == ApiModel.blueprint)
        q = q.filter(RequestModel.endpoint == ApiModel.endpoint)
        q = q.filter(ApiModel.type == 'success')
        if start_time:
            q = q.filter(RequestModel.create_time >= start_time)
        if end_time:
            q = q.filter(RequestModel.create_time <= end_time)
        return q.first()

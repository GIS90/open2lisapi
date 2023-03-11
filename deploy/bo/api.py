# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    api bo
    
base_info:
    __author__ = "PyGo"
    __time__ = "2022/12/29 09:54"
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
# usage: /usr/bin/python api.py
# ------------------------------------------------------------


# ------------------------------------------------------------
# usage: /usr/bin/python template.py
# ------------------------------------------------------------
from sqlalchemy import distinct, func, or_

from deploy.bo.bo_base import BOBase
from deploy.models.api import ApiModel

from deploy.utils.utils import get_now


class ApiBo(BOBase):

    def __init__(self):
        super(ApiBo, self).__init__()

    def new_mode(self):
        return ApiModel()

    def execute_sql(self, sql):
        if not sql:
            return None
        q = self.session.execute(sql)
        return q

    def get_all(self, params: dict):
        q = self.session.query(ApiModel)
        q = q.filter(ApiModel.is_del != 1)
        """多参数高级筛选"""
        if params.get('create_rtx'):  # 创建用户RTX
            q = q.filter(ApiModel.create_rtx.in_(params.get('create_rtx')))
        if params.get('type'):  # API类型
            q = q.filter(ApiModel.type.in_(params.get('type')))
        if params.get('blueprint'):  # blueprint
            q = q.filter(ApiModel.blueprint.like(params.get('blueprint')))
        if params.get('apiname'):  # apiname
            q = q.filter(ApiModel.apiname.like(params.get('apiname')))
        if params.get('content'):  # 模糊查询内容
            q = q.filter(or_(
                ApiModel.blueprint.like(params.get('content')),
                ApiModel.apiname.like(params.get('content')),
                ApiModel.endpoint.like(params.get('content')),
                ApiModel.path.like(params.get('content')),
                ApiModel.short.like(params.get('content')),
                ApiModel.long.like(params.get('content'))
            ))
        if params.get('create_time_start'):  # 起始创建时间
            q = q.filter(ApiModel.create_time >= params.get('create_time_start'))
        if params.get('create_time_end'):  # 结束创建时间
            q = q.filter(ApiModel.create_time <= params.get('create_time_end'))
        q = q.order_by(ApiModel.order_id.asc(), ApiModel.create_time.desc())
        if not q:
            return [], 0
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

    def get_model_by_md5(self, md5_id):
        q = self.session.query(ApiModel)
        q = q.filter(ApiModel.md5_id == str(md5_id))
        return q.first() if q else None

    def batch_delete_by_md5(self, params):
        if not params.get('list'):
            return 0

        md5_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(ApiModel)
        q = q.filter(ApiModel.md5_id.in_(md5_list))
        q = q.filter(ApiModel.is_del != 1)
        q = q.update({ApiModel.is_del: True,
                      ApiModel.delete_rtx: rtx_id,
                      ApiModel.delete_time: get_now()},
                     synchronize_session=False)
        return q

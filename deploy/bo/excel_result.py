# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/4/27 3:03 下午"
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
# usage: /usr/bin/python excel_result.py
# ------------------------------------------------------------

from deploy.bo.bo_base import BOBase
from deploy.models.excel_result import ExcelResultModel
from deploy.models.enum import EnumModel
from deploy.utils.utils import get_now


class ExcelResultBo(BOBase):

    def __init__(self):
        super(ExcelResultBo, self).__init__()

    def new_mode(self):
        return ExcelResultModel()

    def execute_sql(self, sql):
        if not sql:
            return None
        q = self.session.execute(sql)
        return q

    def get_all(self, params: dict):
        q = self.session.query(ExcelResultModel.id,
                               ExcelResultModel.name,
                               ExcelResultModel.store_name,
                               ExcelResultModel.md5_id,
                               ExcelResultModel.rtx_id,
                               ExcelResultModel.ftype,
                               ExcelResultModel.local_url,
                               ExcelResultModel.store_url,
                               ExcelResultModel.is_compress,
                               ExcelResultModel.nfile,
                               ExcelResultModel.nsheet,
                               ExcelResultModel.row,
                               ExcelResultModel.col,
                               ExcelResultModel.sheet_names,
                               ExcelResultModel.sheet_columns,
                               ExcelResultModel.headers,
                               ExcelResultModel.create_time,
                               ExcelResultModel.delete_rtx,
                               ExcelResultModel.delete_time,
                               ExcelResultModel.is_del,
                               EnumModel.name.label('enum_name'),
                               EnumModel.key.label('enum_key'),
                               EnumModel.value.label('enum_value'))
        q = q.filter(ExcelResultModel.ftype == EnumModel.key)
        if params.get('enum_name'):
            q = q.filter(EnumModel.name == str(params.get('enum_name')).lower())
        if params.get('name'):
            q = q.filter(ExcelResultModel.name.like(params.get('name')))
        if params.get('type'):
            q = q.filter(ExcelResultModel.ftype.in_(params.get('type')))
        if params.get('rtx_id'):
            q = q.filter(ExcelResultModel.rtx_id == str(params.get('rtx_id')))
        if params.get('start_time'):
            q = q.filter(ExcelResultModel.create_time >= params.get('start_time'))
        if params.get('end_time'):
            q = q.filter(ExcelResultModel.create_time <= params.get('end_time'))
        q = q.filter(ExcelResultModel.is_del != 1)
        q = q.order_by(ExcelResultModel.create_time.desc())
        if not q:
            return [], 0
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

    def get_model_by_md5(self, md5):
        q = self.session.query(ExcelResultModel)
        q = q.filter(ExcelResultModel.md5_id == str(md5))
        return q.first() if q else None

    def batch_delete_by_md5(self, params):
        if not params.get('list'):
            return 0

        md5_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(ExcelResultModel)
        q = q.filter(ExcelResultModel.md5_id.in_(md5_list))
        if rtx_id:
            q = q.filter(ExcelResultModel.rtx_id == rtx_id)
        q = q.filter(ExcelResultModel.is_del != 1)
        q = q.update({ExcelResultModel.is_del: True,
                      ExcelResultModel.delete_rtx: rtx_id,
                      ExcelResultModel.delete_time: get_now()},
                     synchronize_session=False)
        return q

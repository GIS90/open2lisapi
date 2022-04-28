# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/4/27 3:02 下午"
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
# usage: /usr/bin/python excel_source.py
# ------------------------------------------------------------

from deploy.bo.bo_base import BOBase
from deploy.models.excel_source import ExcelSourceModel
from deploy.models.enum import EnumModel


class ExcelSourceBo(BOBase):

    def __init__(self):
        super(ExcelSourceBo, self).__init__()

    def new_mode(self):
        return ExcelSourceModel()
    
    def get_all(self, params: dict):
        q = self.session.query(ExcelSourceModel.id,
                               ExcelSourceModel.name,
                               ExcelSourceModel.store_name,
                               ExcelSourceModel.md5_id,
                               ExcelSourceModel.rtx_id,
                               ExcelSourceModel.ftype,
                               ExcelSourceModel.local_url,
                               ExcelSourceModel.store_url,
                               ExcelSourceModel.nsheet,
                               ExcelSourceModel.set_sheet,
                               ExcelSourceModel.sheet_names,
                               ExcelSourceModel.sheet_columns,
                               ExcelSourceModel.headers,
                               ExcelSourceModel.create_time,
                               ExcelSourceModel.delete_rtx,
                               ExcelSourceModel.delete_time,
                               ExcelSourceModel.is_del,
                               EnumModel.name.label('enum_name'),
                               EnumModel.key,
                               EnumModel.value)
        q = q.filter(ExcelSourceModel.ftype == EnumModel.key)
        q = q.filter(ExcelSourceModel.is_del != 1)
        if params.get('enum_name'):
            q = q.filter(EnumModel.name == str(params.get('enum_name')).lower())
        if params.get('type'):
            q = q.filter(ExcelSourceModel.ftype == str(params.get('type')))
        if params.get('rtx_id'):
            q = q.filter(ExcelSourceModel.rtx_id == str(params.get('rtx_id')))
        q = q.order_by(ExcelSourceModel.create_time.desc())
        if not q.all():
            return []
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all()

    def get_model_by_md5(self, md5):
        q = self.session.query(ExcelSourceModel)
        q = q.filter(ExcelSourceModel.md5_id == str(md5))
        return q.first() if q else None

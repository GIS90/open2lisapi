# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/6/14 22:17"
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
# usage: /usr/bin/python office.py
# ------------------------------------------------------------

from deploy.bo.bo_base import BOBase
from deploy.models.office_pdf import OfficePDFModel
from deploy.models.enum import EnumModel
from deploy.utils.utils import get_now


class OfficePDFBo(BOBase):

    def __init__(self):
        super(OfficePDFBo, self).__init__()

    def new_mode(self):
        return OfficePDFModel()

    def get_all(self, params: dict):
        q = self.session.query(OfficePDFModel)
        q = q.filter(OfficePDFModel.is_del != 1)
        if params.get('rtx_id'):
            q = q.filter(OfficePDFModel.rtx_id == str(params.get('rtx_id')))
        q = q.order_by(OfficePDFModel.create_time.desc())
        if not q:
            return [], 0
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

    def get_model_by_md5(self, md5):
        q = self.session.query(OfficePDFModel)
        q = q.filter(OfficePDFModel.md5_id == str(md5))
        return q.first() if q else None

    def batch_delete_by_md5(self, params):
        if not params.get('list'):
            return 0

        md5_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(OfficePDFModel)
        q = q.filter(OfficePDFModel.md5_id.in_(md5_list))
        if rtx_id:
            q = q.filter(OfficePDFModel.rtx_id == rtx_id)
        q = q.filter(OfficePDFModel.is_del != 1)
        q = q.update({OfficePDFModel.is_del: True,
                      OfficePDFModel.delete_rtx: rtx_id,
                      OfficePDFModel.delete_time: get_now()},
                     synchronize_session=False)
        return q

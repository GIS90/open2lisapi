# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    Sqlbase Bo

base_info:
    __author__ = "PyGo"
    __time__ = "2022/12/21 20:39"
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
# usage: /usr/bin/python sqlbase.py
# ------------------------------------------------------------
from sqlalchemy import distinct, func, or_

from deploy.bo.bo_base import BOBase
from deploy.model.sqlbase import SqlbaseModel
from deploy.model.enum import EnumModel

from deploy.utils.utils import get_now


class SqlbaseBo(BOBase):

    def __init__(self):
        super(SqlbaseBo, self).__init__()

    def __str__(self):
        return "Sqlbase Bo."

    def __repr__(self):
        return self.__str__()

    def new_mode(self):
        return SqlbaseModel()

    def get_all(self, params: dict):
        q = self.session.query(SqlbaseModel.id,
                               SqlbaseModel.rtx_id,
                               SqlbaseModel.title,
                               SqlbaseModel.md5_id,
                               SqlbaseModel.author,
                               SqlbaseModel.recommend,
                               SqlbaseModel.database,
                               SqlbaseModel.summary,
                               SqlbaseModel.label,
                               SqlbaseModel.public,
                               SqlbaseModel.public_time,
                               SqlbaseModel.html,
                               SqlbaseModel.text,
                               SqlbaseModel.count,
                               SqlbaseModel.create_time,
                               SqlbaseModel.delete_rtx,
                               SqlbaseModel.delete_time,
                               SqlbaseModel.is_del,
                               EnumModel.value.label('enum_value'))
        q = q.filter(SqlbaseModel.database == EnumModel.key)
        q = q.filter(SqlbaseModel.is_del != 1)
        if params.get('enum_name'):
            q = q.filter(EnumModel.name == str(params.get('enum_name')).lower())
        if params.get('public'):
            q = q.filter(SqlbaseModel.public == True)
        if not params.get('public'):
            q = q.filter(SqlbaseModel.public == False)
        # if params.get('rtx_id'):
        #     q = q.filter(SqlbaseModel.rtx_id == str(params.get('rtx_id')))
        """多参数高级筛选"""
        if params.get('create_rtx'):    # 创建用户RTX
            q = q.filter(SqlbaseModel.rtx_id.in_(params.get('create_rtx')))
        if params.get('author'):    # 作者
            q = q.filter(SqlbaseModel.author.in_(params.get('author')))
        if params.get('recommend'):    # 推荐度
            q = q.filter(SqlbaseModel.recommend.in_(params.get('recommend')))
        if params.get('database'):  # 数据库
            q = q.filter(SqlbaseModel.database.in_(params.get('database')))
        if params.get('label'):    # 标签
            q = q.filter(SqlbaseModel.label.in_(params.get('label')))
        if params.get('content'):  # 内容
            q = q.filter(or_(
                SqlbaseModel.title.like(params.get('content')),
                SqlbaseModel.text.like(params.get('content'))
            ))
        if params.get('create_time_start'):  # 起始创建时间
            q = q.filter(SqlbaseModel.create_time >= params.get('create_time_start'))
        if params.get('create_time_end'):  # 结束创建时间
            q = q.filter(SqlbaseModel.create_time <= params.get('create_time_end'))
        if params.get('public_time_start'):  # 起始发布时间
            q = q.filter(SqlbaseModel.public_time >= params.get('public_time_start'))
        if params.get('public_time_end'):  # 结束发布时间
            q = q.filter(SqlbaseModel.public_time <= params.get('public_time_end'))
        if params.get('count_start'):  # 浏览次数上限
            q = q.filter(SqlbaseModel.count >= params.get('count_start'))
        if params.get('count_end'):  # 浏览次数下限
            q = q.filter(SqlbaseModel.count <= params.get('count_end'))
        q = q.order_by(SqlbaseModel.create_time.desc())
        if not q:
            return [], 0
        total = len(q.all())
        if params.get('offset'):
            q = q.offset(params.get('offset'))
        if params.get('limit'):
            q = q.limit(params.get('limit'))
        return q.all(), total

    def get_model_by_md5(self, md5):
        q = self.session.query(SqlbaseModel)
        q = q.filter(SqlbaseModel.md5_id == str(md5))
        return q.first() if q else None

    def batch_delete_by_md5(self, params):
        if not params.get('list'):
            return 0

        md5_list = params.get('list')
        rtx_id = params.get('rtx_id')
        q = self.session.query(SqlbaseModel)
        q = q.filter(SqlbaseModel.md5_id.in_(md5_list))
        if rtx_id:
            q = q.filter(SqlbaseModel.rtx_id == rtx_id)
        q = q.filter(SqlbaseModel.is_del != 1)
        q = q.update({SqlbaseModel.is_del: True,
                      SqlbaseModel.delete_rtx: rtx_id,
                      SqlbaseModel.delete_time: get_now()},
                     synchronize_session=False)
        return q

# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/12/21 18:24"
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
# usage: /usr/bin/python search.py
# ------------------------------------------------------------
import json

from deploy.bo.sqlbase import SqlbaseBo

from deploy.config import OFFICE_LIMIT, ADMIN
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import d2s, get_now, md5, check_length


class SearchService(object):
    """
    search service
    """

    req_sqlbase_list_attrs = [
        'rtx_id',
        'limit',
        'offset',
        'public'
    ]

    sqlbase_list_attrs = [
        # 'id',
        'rtx_id',
        'title',
        'md5_id',
        'author',
        'recommend',
        'summary',
        'public',
        'public_time',
        'content',
        'create_time',
        'delete_rtx',
        'delete_time',
        'is_del'
    ]

    req_sqlbase_add_attrs = [
        'rtx_id',
        'title',
        'author',
        'recommend',
        'summary',
        'label',
        'public',
        'public_time',
        'content',
    ]

    req_sqlbase_add_no_need_attrs = [
        'summary',
        'label'
    ]

    req_sqlbase_add_ck_len_attrs = {
        'rtx_id': 25,
        'title': 55,
        'author': 25,
        'summary': 200
    }


    def __init__(self):
        """
        search service class initialize
        """
        self.sqlbase_bo = SqlbaseBo()

    def _transfer_time(self, t):
        if not t:
            return ""

        if not isinstance(t, str):
            return d2s(t)
        elif isinstance(t, str) and t == '0000-00-00 00:00:00':
            return ""
        else:
            return t or ''

    def _sqlbase_model_to_dict(self, model) -> dict:
        """
        sqlbase model object transfer to dict type
        """
        if not model:
            return {}
        _res = dict()
        for attr in self.sqlbase_list_attrs:
            if not attr: continue
            if attr == 'id':
                _res[attr] = model.id
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id
            elif attr == 'title':
                _res[attr] = model.title
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'author':
                _res[attr] = model.author
            elif attr == 'recommend':
                _res[attr] = model.recommend
            elif attr == 'summary':
                _res[attr] = model.summary
            elif attr == 'public':
                _res[attr] = model.public
            elif attr == 'public_time':
                _res[attr] = self._transfer_time(model.public_time)
            elif attr == 'content':
                _res[attr] = model.content
            elif attr == 'create_time':
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'delete_rtx':
                _res[attr] = model.delete_rtx or ""
            elif attr == 'delete_time':
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'is_del':
                _res[attr] = True if model.is_del else False
        else:
            return _res

    def sqlbase_list(self, params: dict) -> json:
        """
        get sqlbase list by params
        params is dict
        return json data
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_sqlbase_list_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if k == 'limit':
                v = int(v) if v else OFFICE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            elif k == 'public':
                v = True if v else False
            else:
                v = str(v) if v else ''
            new_params[k] = v
        # **************** 管理员获取ALL数据 *****************
        if new_params.get('rtx_id') == ADMIN:
            new_params.pop('rtx_id')
        # <get data>
        res, total = self.sqlbase_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # ////////////////// return data \\\\\\\\\\\\\\\\\\\\\
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._sqlbase_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def sqlbase_add(self, params: dict) -> dict:
        """
        add new data to db table sqlbase, new data is dict object
        :return: json data
        """
        # ===== check parameters && format parameters ======
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_sqlbase_add_attrs:
                return Status(
                    213, 'failure', '请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in self.req_sqlbase_add_no_need_attrs:  # is not null
                return Status(
                    214, 'failure', '请求参数%s为必须信息' % k, {}).json()
            new_params[k] = v
        # parameters length check
        for _key, _value in self.req_sqlbase_add_ck_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # create new model
        new_model = self.sqlbase_bo.new_mode()
        # 默认值
        new_params['md5_id'] = md5(new_params.get('title')+get_now()+new_params.get('rtx_id'))
        new_params['create_time'] = get_now()
        new_params['is_del'] = False
        for key, value in new_params.items():
            if not key: continue
            setattr(new_model, key, value)
        else:
            self.sqlbase_bo.add_model(new_model)

        return Status(
            100, 'success', StatusMsgs.get(100), {}).json()

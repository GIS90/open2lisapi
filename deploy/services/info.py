# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    information service

base_info:
    __author__ = "PyGo"
    __time__ = "2022/8/30 21:31"
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
# usage: /usr/bin/python info.py
# ------------------------------------------------------------
from operator import itemgetter
from itertools import groupby

from deploy.bo.enum import EnumBo
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import d2s, get_now


class InfoService(object):
    """
    information service
    """

    PAGE_LIMIT = 15

    req_dict_list_attrs = [
        'rtx_id',
        'limit',
        'offset'
    ]

    dict_list_attrs = [
        'name',
        'md5_id',
        'key',
        'value',
        'description',
        'status',
        'create_rtx',
        'create_time',
        'update_rtx',
        'update_time',
        'delete_rtx',
        'delete_time',
        'is_del',
        'order_id'
    ]

    req_dict_status_attrs = [
        'rtx_id',
        'md5',
        'status'
    ]

    req_delete_attrs = [
        'rtx_id',
        'md5'
    ]

    def __init__(self):
        """
        information service class initialize
        """
        super(InfoService, self).__init__()
        self.enum_bo = EnumBo()

    def _enum_model_to_dict(self, model, _type='list'):
        """
        enum model transfer to dict data
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.dict_list_attrs:
            if not attr: continue
            if attr == 'name':
                _res[attr] = model.name if getattr(model, 'name') else ""
            elif attr == 'md5_id':
                _res['md5'] = model.md5_id if getattr(model, 'md5_id') else ""
            elif attr == 'key':
                _res[attr] = model.key if getattr(model, 'key') else ""
            elif attr == 'value':
                _res[attr] = model.value if getattr(model, 'value') else ""
            elif attr == 'description':
                _res[attr] = model.description if getattr(model, 'description') else ""
            elif attr == 'status':
                _res[attr] = True if getattr(model, 'status') else False
            elif attr == 'create_rtx':
                _res[attr] = model.create_rtx if getattr(model, 'create_rtx') else ""
            elif attr == 'create_time':
                _time = model.create_time if getattr(model, 'create_time') else ""
                if _time == '0000-00-00 00:00:00':
                    _res[attr] = ''
                    continue
                _res[attr] = _time if isinstance(_time, str) else d2s(_time)
            elif attr == 'update_rtx':
                _res[attr] = model.update_rtx if getattr(model, 'update_rtx') else ""
            elif attr == 'update_time':
                _time = model.update_time if getattr(model, 'update_time') else ""
                if _time == '0000-00-00 00:00:00':
                    _res[attr] = ''
                    continue
                _res[attr] = _time if isinstance(_time, str) else d2s(_time)
            elif attr == 'delete_rtx':
                _res[attr] = model.delete_rtx if getattr(model, 'delete_rtx') else ""
            elif attr == 'delete_time':
                _time = model.delete_time if getattr(model, 'delete_time') else ""
                if _time == '0000-00-00 00:00:00':
                    _res[attr] = ''
                    continue
                _res[attr] = _time if isinstance(_time, str) else d2s(_time)
            elif attr == 'is_del':
                _res[attr] = True if getattr(model, 'is_del') else False
            elif attr == 'order_id':
                _res[attr] = model.order_id if getattr(model, 'order_id') else 1
        else:
            return _res

    def dict_list(self, params: dict) -> dict:
        """
        dict list by params
        params is dict
        return json data
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_dict_list_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if k == 'limit':
                v = int(v) if v else self.PAGE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            else:
                v = str(v) if v else ''
            new_params[k] = v

        # **************** <get data> *****************
        res, total = self.enum_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # <<<<<<<<<<<<<<<<<<<< format and return data >>>>>>>>>>>>>>>>>>>>
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._enum_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def dict_status(self, params: dict) -> dict:
        """
        change dict data status by md5
        :return: json data

        状态改变：
        true：启用
        false：禁用
        """
        # not parameters
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        # parameters check and format
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_dict_status_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v and k != 'status':     # value check, is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            if k == 'status':   # status check: 只允许为bool类型
                if not isinstance(v, bool):
                    return Status(
                        214, 'failure', u'请求参数%s类型不符合要求' % k, {}).json()
                new_params[k] = v
            else:
                new_params[k] = str(v)
        # <<<<<<<<<<<<< get and check data model >>>>>>>>>>>>>>>
        model = self.enum_bo.get_model_by_md5(md5_id=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                304, 'failure', '数据已删除，不允许设置' or StatusMsgs.get(304), {}).json()
        # ----------- change status -----------
        print(new_params)
        model.status = new_params.get('status')
        model.update_rtx = new_params.get('rtx_id')
        model.update_time = get_now()
        self.enum_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def dict_delete(self, params: dict):
        """
        delete one dict data status by md5
        params is dict
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_delete_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)

        # ====================== data check ======================
        model = self.enum_bo.get_model_by_md5(md5_id=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}).json()
        # <update data>
        setattr(model, 'is_del', True)
        setattr(model, 'delete_rtx', new_params.get('rtx_id'))
        setattr(model, 'delete_time', get_now())
        self.enum_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

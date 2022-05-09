# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    authority services

base_info:
    __author__ = "PyGo"
    __time__ = "2022/5/9 22:53"
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
# usage: /usr/bin/python authority.py
# ------------------------------------------------------------
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.status import Status
from deploy.bo.role import RoleBo

from deploy.config import AUTH_LIMIT, AUTH_NUM


class AuthorityService(object):
    """
    authority service
    """

    req_role_list_attrs = [
        'rtx_id',
        'limit',
        'offset'
    ]

    list_attrs = [
        'id',
        'engname',
        'chnname',
        'md5_id',
        'authority',
        'introduction',
        'create_time',
        'create_operator',
        'del_time',
        'del_operator',
        'is_del'
    ]

    def __init__(self):
        """
        authority service class initialize
        """
        super(AuthorityService, self).__init__()
        self.role_bo = RoleBo()

    def _role_model_to_dict(self, model):
        """
        role model to dict data
        return json data
        """
        if not model:
            return {}

        res = dict()
        for attr in self.list_attrs:
            if not attr:continue
            if attr == 'engname':
                res[attr] = model.engname
            elif attr == 'chnname':
                res[attr] = model.chnname
            elif attr == 'md5_id':
                res[attr] = model.md5_id
            elif attr == 'authority':
                res[attr] = model.authority
            elif attr == 'introduction':
                res[attr] = model.introduction
            elif attr == 'create_time':
                res[attr] = model.create_time
            elif attr == 'create_operator':
                res[attr] = model.create_operator
            elif attr == 'del_time':
                res[attr] = model.del_time
            elif attr == 'del_operator':
                res[attr] = model.del_operator
            elif attr == 'is_del':
                res[attr] = model.is_del
        else:
            return res

    def role_list(self, params):
        """
        get role list, many parameters
        return json data

        default get role is no delete
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_role_list_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}
                ).json()
            if k == 'limit':
                v = int(v) if v else AUTH_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            else:
                v = str(v)
            new_params[k] = v

        res, total = self.role_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}
            ).json()
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._role_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

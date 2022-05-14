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
import datetime

from deploy.utils.status_msg import StatusMsgs
from deploy.utils.status import Status
from deploy.bo.role import RoleBo

from deploy.config import AUTH_LIMIT, AUTH_NUM, ADMIN
from deploy.utils.utils import d2s, get_now, md5


class AuthorityService(object):
    """
    authority service
    """

    req_role_list_attrs = [
        'rtx_id',
        'limit',
        'offset'
    ]

    req_role_add_attrs = [
        'rtx_id',
        'engname',
        'chnname',
        'introduction'
    ]

    req_role_update_attrs = [
        'rtx_id',
        'md5',
        'engname',
        'chnname',
        'introduction'
    ]

    list_attrs = [
        'id',
        'engname',
        'chnname',
        'md5_id',
        'authority',
        'introduction',
        'create_time',
        'create_rtx',
        'delete_time',
        'delete_rtx',
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
                if model.create_time and isinstance(model.create_time, str):
                    res[attr] = model.create_time
                elif model.create_time and isinstance(model.create_time, datetime.datetime):
                    res[attr] = d2s(model.create_time)
                else:
                    res[attr] = ''
            elif attr == 'create_rtx':
                res[attr] = model.create_rtx
            elif attr == 'delete_time':
                if model.delete_time and isinstance(model.delete_time, str):
                    res[attr] = model.delete_time
                elif model.delete_time and isinstance(model.delete_time, datetime.datetime):
                    res[attr] = d2s(model.delete_time)
                else:
                    res[attr] = ''
            elif attr == 'delete_rtx':
                res[attr] = model.delete_rtx
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
            if not v and k != 'offset':
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

    def role_add(self, params):
        """
        add new role, information contain: english name, chinese name, introduction
        :return: json data

        new data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_role_add_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}
                ).json()
            # check: length
            if k == 'engname' and len(v) > 25:
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'engname' and len(v) > 25:
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'introduction' and len(v) > 55:
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            new_params[k] = str(v)

        # check engname is or not repeat
        model = self.role_bo.get_model_by_engname(new_params.get('engname'))
        if model:
            return Status(
                213, 'failure', '角色RTX已存在，请重新输入', {}
            ).json()

        new_model = self.role_bo.new_mode()
        new_model.engname = new_params.get('engname')
        new_model.chnname = new_params.get('chnname')
        md5_id = md5(new_params.get('engname'))
        new_model.md5_id = md5_id
        new_model.authority = ''
        new_model.introduction = new_params.get('introduction')
        new_model.create_time = get_now()
        new_model.create_rtx = new_params.get('rtx_id')
        new_model.is_del = False
        self.role_bo.add_model(new_model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': md5_id}
        ).json()

    def role_update(self, params):
        """
        update role, information contain: chinese name, introduction
        by role md5
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_role_update_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}
                ).json()
            # check: length
            if k == 'engname' and len(v) > 25:
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'engname' and len(v) > 25:
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'introduction' and len(v) > 55:
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            new_params[k] = str(v)

        if new_params.get('engname') == ADMIN:
            return Status(
                213, 'failure', u'AMDIN角色为系统默认角色，不允许操作', {}
            ).json()

        # check engname is or not repeat
        model = self.role_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在', {}
            ).json()
        # data is delete
        if model and model.is_del:
            return Status(
                304, 'failure', '数据已删除，不允许更新', {}
            ).json()

        model.chnname = new_params.get('chnname')
        model.introduction = new_params.get('introduction')
        self.role_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def role_batch_delete(self, params):
        """
        batch delete many role data, from role table
        post request and json parameters
        :return: json data
        """
        pass

    def role_delete(self, params):
        """
        one delete many role data
        from role table
        post request and json parameters
        :return: json data
        """
        pass
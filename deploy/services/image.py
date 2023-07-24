# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2023/7/20 23:23"
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
# usage: /usr/bin/python image.py
# ------------------------------------------------------------
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import d2s, s2d

from deploy.bo.sysuser_avatar import SysUserAvatarModelBo


class ImageService(object):
    """
    image service
    """

    PAGE_LIMIT = 15

    # 用户
    req_user_necessary_attrs = ['rtx_id']

    # 数据md5
    req_md5_necessary_attrs = ['rtx_id', 'md5']

    # list api
    req_list_necessary_attrs = ['rtx_id', 'limit', 'offset']

    # define many request api parameters
    # 分页数据通用请求参数
    req_page_comm_attrs = [
        'rtx_id',
        'limit',
        'offset'
    ]

    sysuser_avatar_list_attrs = [
        # 'id',
        'rtx_id',
        'md5_id',
        'name',
        'summary',
        'label',
        'url',
        'count',
        'create_time',
        'update_rtx',
        'update_time',
        'delete_rtx',
        'delete_time',
        'is_del',
        'order_id'
    ]

    def __init__(self):
        """
        information service class initialize
        """
        super(ImageService, self).__init__()
        self.sysuser_avatar_bo = SysUserAvatarModelBo()

    @staticmethod
    def _transfer_time(t):
        if not t:
            return ""

        if not isinstance(t, str):
            return d2s(t)
        elif isinstance(t, str) and t == '0000-00-00 00:00:00':
            return ""
        else:
            return t or ''

    def _sysuer_avatar_model_to_dict(self, model, _type='list'):
        """
        enum model transfer to dict data
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.sysuser_avatar_list_attrs:
            if not attr: continue
            if attr == 'id' and _type in ['list']:
                _res[attr] = getattr(model, 'id', '')
            elif attr == 'name' and _type in ['list']:
                _res[attr] = getattr(model, 'name', '')
            elif attr == 'md5_id' and _type in ['list', 'avatar']:
                _res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'rtx_id' and _type in ['list']:
                _res[attr] = getattr(model, 'rtx_id', '')
            elif attr == 'summary' and _type in ['list']:
                _res[attr] = getattr(model, 'summary', '')
            elif attr == 'label' and _type in ['list']:
                _res[attr] = getattr(model, 'label', '')
            elif attr == 'url' and _type in ['list', 'avatar']:
                _res[attr] = getattr(model, 'url', '')
            elif attr == 'count' and _type in ['list']:
                _res[attr] = getattr(model, 'count', 0)
            elif attr == 'create_time' and _type in ['list']:
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'update_rtx' and _type in ['list']:
                _res[attr] = getattr(model, 'update_rtx', '')
            elif attr == 'update_time' and _type in ['list']:
                _res[attr] = self._transfer_time(model.update_time)
            elif attr == 'delete_rtx' and _type in ['list']:
                _res[attr] = getattr(model, 'delete_rtx', '')
            elif attr == 'delete_time' and _type in ['list']:
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'is_del' and _type in ['list']:
                _res[attr] = model.is_del or False
            elif attr == 'order_id' and _type in ['list']:
                _res[attr] = getattr(model, 'order_id', 1)
        else:
            return _res

    def profile_avatar_list(self, params: dict) -> dict:
        """
        get profile avatar data list by params
        params is dict
        return json data
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_page_comm_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_page_comm_attrs and v:
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
        rtx_id = new_params.get('rtx_id')
        # 全量
        new_params.pop('rtx_id')
        res, total = self.sysuser_avatar_bo.get_all(new_params)
        # no data
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # <<<<<<<<<<<<<<<<<<<< format and return data >>>>>>>>>>>>>>>>>>>>
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._sysuer_avatar_model_to_dict(_d, _type='avatar')
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()


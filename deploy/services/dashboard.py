# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/8/19 15:31"
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
# usage: /usr/bin/python dashboard.py
# ------------------------------------------------------------
from deploy.bo.sysuser import SysUserBo
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs


class DashboardService(object):
    """
    dashboard service
    """
    req_pan_attrs = [
        'rtx_id'
    ]

    def __init__(self):
        """
        dashboard service class initialize
        """
        self.sysuser_bo = SysUserBo()

    def pan(self, params: dict) -> dict:
        """
        get dashboard pan base information
        contain:
            - user 用户
            -
            -
            -
        """
        # ================= parameters check and format ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_pan_attrs:     # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<<< get return data >>>>>>>>>>>>>>>
        rtx_id = new_params.get('rtx_id')
        ret_res_json = {
            'user': self.sysuser_bo.get_count()
        }
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), ret_res_json
        ).json()


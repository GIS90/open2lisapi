# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    request service

base_info:
    __author__ = "PyGo"
    __time__ = "2022/3/2 10:50 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "twtoolbox_isapi"

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
# usage: /usr/bin/python request.py
# ------------------------------------------------------------
from deploy.bo.request import RequestBo
from deploy.utils.utils import get_now, get_real_ip, \
    get_rtx_id, d2s
from deploy.config import USER_DEFAULT_TIMELINE, OFFICE_LIMIT
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs


class RequestService(object):

    req_list_attrs = [
        'rtx_id',
        'limit',
        'offset'
    ]

    def __init__(self):
        """
        initialize
        """
        super(RequestService, self).__init__()
        self.request_bo = RequestBo()
        self.all_attrs = [
            'id',
            'rtx_id',
            'ip',
            'blueprint',
            'endpoint',
            'method',
            'path',
            'full_path',
            'host_url',
            'url',
            'create_time',
        ]
        self.timeline_attrs = [
            'id',
            'path',
            'url',
            'create_time',
            'short',
            'long',
            'type'
        ]

    def _model_to_dict(self, model, _type='timeline'):
        """
        request model to dict data
        """
        if not model:
            return None

        _res = dict()
        if _type == 'timeline':
            for attr in self.timeline_attrs:
                if attr == 'id':
                    _res[attr] = model.id or ""
                elif attr == 'rtx_id':
                    _res[attr] = model.rtx_id or ""
                elif attr == 'url':
                    _res['url'] = model.url or ""
                elif attr == 'create_time':
                    _res['timestamp'] = d2s(model.create_time) if model.create_time else ''
                elif attr == 'type':
                    _res['type'] = model.type or "success"
                elif attr == 'short':
                    _res['title'] = model.short or ""
                elif attr == 'long':
                    _res['content'] = model.long or ""
            else:
                return _res

        for attr in self.all_attrs:
            if attr == 'id':
                _res[attr] = model.id or ""
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id or ""
            elif attr == 'ip':
                _res[attr] = model.ip or ""
            elif attr == 'blueprint':
                _res[attr] = model.blueprint or ""
            elif attr == 'endpoint':
                _res[attr] = model.endpoint or ""
            elif attr == 'method':
                _res[attr] = model.method or ""
            elif attr == 'path':
                _res[attr] = model.path or ""
            elif attr == 'full_path':
                _res[attr] = model.full_path or ""
            elif attr == 'host_url':
                _res[attr] = model.host_url or ""
            elif attr == 'url':
                _res[attr] = model.url or ""
            elif attr == 'create_time':
                _res[attr] = d2s(model.create_time) if model.create_time else ''
        else:
            return _res

    def add_request(self, request, rtx=None) -> bool:
        """
        add request data to db
        """
        if not request:
            return False
        rtx_id = get_rtx_id(request) or rtx
        if not rtx_id:
            return False
        method = request.method
        if method and str(method).upper() not in ['GET', 'POST']:
            return False

        new_model = self.request_bo.new_mode()
        new_model.rtx_id = rtx_id
        new_model.ip = get_real_ip(request)
        new_model.blueprint = request.blueprint if request.blueprint else ''
        new_model.endpoint = request.endpoint if request.endpoint else ''
        new_model.method = str(method).upper() if method else ''
        new_model.path = request.path if request.path else ''
        new_model.full_path = request.full_path if request.full_path else ''
        new_model.host_url = request.host_url if request.host_url else ''
        new_model.url = request.url if request.url else ''
        new_model.create_time = get_now()
        self.request_bo.add_model(new_model)

    def get_by_rtx(self, params) -> dict:
        """
        git request list by rtx_id
        many request dict data

        return json data
        采用分页方式
        """
        if not params:
            return Status(
                212, 'failure', u'缺少请求参数', {}).json()
        # check parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_list_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if k == 'limit':
                v = int(v) if v else OFFICE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            elif k == 'rtx_id':
                v = str(v).strip()
            else:
                v = str(v)
            new_params[k] = v

        # 加上计算时间
        # import datetime
        # start = datetime.datetime.now()
        res, total = self.request_bo.get_by_rtx(new_params)
        # end = datetime.datetime.now()
        # print('=' * 30)
        # print((end-start).seconds)
        # print(total)
        # print('=' * 30)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'timeline': [], 'total': 0}).json()

        data_list = list()
        for d in res:
            if not d: continue
            _d = self._model_to_dict(d, _type='timeline')
            if _d: data_list.append(_d)

        return Status(
            100, 'success',
            StatusMsgs.get(100), {'timeline': data_list, 'total': total}
        ).json()




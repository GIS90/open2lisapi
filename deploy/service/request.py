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
# usage: /usr/bin/python request.py
# ------------------------------------------------------------
from deploy.bo.request import RequestBo
from deploy.utils.utils import get_now, get_real_ip, \
    get_rtx_id, d2s
from deploy.config import USER_DEFAULT_TIMELINE, OFFICE_LIMIT
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs


class RequestService(object):
    """
    request service
    """

    req_list_attrs = [
        'rtx_id',
        'limit',
        'offset'
    ]

    all_attrs = [
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

    timeline_attrs = [
        'id',
        'path',
        'url',
        'create_time',
        'short',
        'long',
        'type'
    ]

    def __init__(self):
        """
        RequestService class initialize
        """
        super(RequestService, self).__init__()
        # bo
        self.request_bo = RequestBo()

    def __str__(self):
        print("RequestService class.")

    def __repr__(self):
        self.__str__()

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
                    _res[attr] = getattr(model, 'id', '')
                elif attr == 'rtx_id':
                    _res[attr] = getattr(model, 'rtx_id', '')
                elif attr == 'url':
                    _res['url'] = getattr(model, 'url', '')
                elif attr == 'create_time':
                    _res['timestamp'] = self._transfer_time(model.create_time)
                elif attr == 'type':
                    _res['type'] = getattr(model, 'type', 'success')
                elif attr == 'short':
                    _res['title'] = getattr(model, 'short', '')
                elif attr == 'long':
                    _res['content'] = getattr(model, 'long', '')
            else:
                return _res

        for attr in self.all_attrs:
            if attr == 'id':
                _res[attr] = getattr(model, 'id', '')
            elif attr == 'rtx_id':
                _res[attr] = getattr(model, 'rtx_id', '')
            elif attr == 'ip':
                _res[attr] = getattr(model, 'ip', '')
            elif attr == 'blueprint':
                _res[attr] = getattr(model, 'blueprint', '')
            elif attr == 'endpoint':
                _res[attr] = getattr(model, 'endpoint', '')
            elif attr == 'method':
                _res[attr] = getattr(model, 'method', '')
            elif attr == 'path':
                _res[attr] = getattr(model, 'path', '')
            elif attr == 'full_path':
                _res[attr] = getattr(model, 'full_path', '')
            elif attr == 'host_url':
                _res[attr] = getattr(model, 'host_url', '')
            elif attr == 'url':
                _res[attr] = getattr(model, 'url', '')
            elif attr == 'create_time':
                _res[attr] = self._transfer_time(model.create_time)
        else:
            return _res

    def add_request(self, request, cost=0, rtx=None) -> bool:
        """
        API request information to insert into database table [request]
        :param request: API request object parameters
        :param cost: API run time, unit is second
        :param rtx: request user rtx-id
            - 1.request get "X-Rtx-Id"
            - 2.no request by manual set

        方法调用主要2来源：
            - 1.manage > 手动记录login in, login out
            - 2.watcher > 打点
        """
        if not request:     # no request, return
            return False
        rtx_id = get_rtx_id(request) or rtx  # not rtx_id, no insert
        if not rtx_id:
            return False
        method = getattr(request, 'method')  # method allow only get or post
        if method and str(method).upper() not in ['GET', 'POST']:
            return False

        new_model = self.request_bo.new_mode()
        new_model.rtx_id = rtx_id
        new_model.ip = get_real_ip(request)  # API request real ip
        new_model.blueprint = request.blueprint if getattr(request, 'blueprint') else ''
        new_model.apiname = str(request.endpoint).split('.')[-1] if getattr(request, 'endpoint') else ''
        new_model.endpoint = request.endpoint if getattr(request, 'endpoint') else ''
        new_model.method = str(method).upper()
        new_model.path = request.path if getattr(request, 'path') else ''
        new_model.full_path = request.full_path if getattr(request, 'full_path') else ''
        new_model.host_url = request.host_url if getattr(request, 'host_url') else ''
        new_model.url = request.url if getattr(request, 'url') else ''
        new_model.cost = cost
        new_model.create_time = get_now()
        new_model.create_date = get_now(format="%Y-%m-%d")
        self.request_bo.add_model(new_model)

    def get_by_rtx(self, params) -> dict:
        """
        git request list by rtx_id
        many request dict data

        return json data
        采用分页方式
        """
        # >>>>>>>>>>>>>>>>> no parameters <<<<<<<<<<<<<<<<<<
        if not params:
            return Status(
                212, 'failure', u'缺少请求参数', {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_list_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
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




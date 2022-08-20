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
from collections import OrderedDict

from deploy.utils.utils import get_now, get_day_week_date, get_now_date, \
    d2s
from deploy.bo.sysuser import SysUserBo
from deploy.bo.request import RequestBo
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs


class DashboardService(object):
    """
    dashboard service
    """
    req_pan_attrs = [
        'rtx_id'
    ]

    req_pan_chart_attrs = [
        'rtx_id',
        'type'
    ]

    req_index_chart_attrs = [
        'rtx_id',
        'type'
    ]

    def __init__(self):
        """
        dashboard service class initialize
        """
        self.sysuser_bo = SysUserBo()
        self.request_bo = RequestBo()

    def pan(self, params: dict) -> dict:
        """
        dashboard pan chart data
        contain:
        pan:
            - user 用户
            - click 点击率
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
        # ---------------- parameter initialize ----------------
        rtx_id = new_params.get('rtx_id')
        now_date = get_now(format="%Y-%m-%d")
        date_params = {
            "start_time": "%s 00:00:00" % now_date,
            "end_time": "%s 23:59:59" % now_date
        }
        # <<<<<<<<<<<<<<<< get return pan: user >>>>>>>>>>>>>>>
        # 总用户数
        # user = self.sysuser_bo.get_count() or 1
        # 当日登录用户数
        user = self.request_bo.get_user_count_by_time(date_params) or 1
        # <<<<<<<<<<<<<<<< get return pan: click >>>>>>>>>>>>>>>
        request = self.request_bo.get_req_count_by_time(date_params) or 0
        ret_res_json = {
            'user': user,
            'click': request
        }
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), ret_res_json
        ).json()

    def pan_chart(self, params: dict) -> dict:
        """
        get dashboard pan chart data
        contain:
            - user 用户
            - click 点击率
        """
        # ================= parameters check and format ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_pan_chart_attrs:     # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)
        # ---------------- parameter initialize ----------------
        rtx_id = new_params.get('rtx_id')
        _type = new_params.get('type')
        week = get_day_week_date(get_now_date())
        date_params = {
            "start_date": week.get('start_week_date'),
            "end_date": week.get('end_week_date')
        }
        if _type == 'user':
            # <<<<<<<<<<<<<<<< get return user 本周 >>>>>>>>>>>>>>>
            # 当日登录用户数 用sql进行查询
            _sql = """
            select 
                create_date, count(1)
            from (
                select 
                    create_date as create_date, rtx_id as rtx_id
                from request
                where create_date BETWEEN '%s' and '%s'
                group by create_date, rtx_id
            )t
            group by create_date
            order by create_date asc
            """ % (date_params.get('start_date'), date_params.get('end_date'))
            ret_res = self.request_bo.execute_sql(_sql)
        elif _type == 'click':
            # <<<<<<<<<<<<<<<< get return click 本周 >>>>>>>>>>>>>>>
            ret_res = self.request_bo.get_req_count_by_week(date_params) or 0
        else:
            ret_res = list()
        # -------------- 格式化数据 --------------
        """
        1.创建一个有序字典，里面星期数据初始化为0
        2.遍历数据，更新有序字典星期数据
        3.把星期数据遍历到列表
        4.return
        """
        _ret_week_dict = OrderedDict()
        for day in week.get('week_date'):   # 初始化数据，默认为0
            if not day: continue
            _ret_week_dict[day] = 0
        """ ======== 在ret_res不为空情况下进行遍历 ======== """
        if ret_res:
            for _r in ret_res:  # 遍历每一个指定格式数据：date count
                if not _r: continue
                _date = _r[0]
                if not isinstance(_date, str):      # 转换日期为str类型
                    _date = d2s(_date, fmt="%Y-%m-%d")
                if _date in _ret_week_dict.keys():  # 存在 && 更新
                    _ret_week_dict[_date] = _r[1]
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), list(_ret_week_dict.values())
        ).json()

    def _get_index_one(self):
        func_names = {
            'office.excel_merge': "表格合并",
            'office.excel_split': "表格拆分",
            'office.office_pdf_to': "PDF转WORD",
            'notify.dtalk_send': "钉钉绩效"
        }
        _res = self.request_bo.get_func_count(params={'func_names': list(func_names.keys())})
        _ret_dict = OrderedDict()
        for key in func_names.keys():  # 初始化数据，默认为0
            if not key: continue
            _ret_dict[key] = 0
        """ ======== 在ret_res不为空情况下进行遍历 ======== """
        if _res:
            for _r in _res:  # 遍历每一个指定格式数据：date count
                if not _r: continue
                _k = _r[0]
                if _k in _ret_dict.keys():  # 存在 && 更新
                    _ret_dict[_k] = _r[1]
        _ret_res = list()
        for k, v in _ret_dict.items():
            if not k: continue
            _ret_res.append({"name": func_names.get(k), "value": v})
        return _ret_res

    def index(self, params: dict) -> dict:
        """
        dashboard index chart data initialize
        指标数据 contain:
        index one 指标一：功能使用率
        index two 指标二：
        index three 指标三：
        """
        # ================= parameters check and format ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_index_chart_attrs:     # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)
        # ---------------- parameter initialize ----------------
        rtx_id = new_params.get('rtx_id')
        _type = new_params.get('type')
        ret_res_json = list()
        # <<<<<<<<<<<<<<<< get return index: 功能使用率 >>>>>>>>>>>>>>>
        if _type == '1':
            ret_res_json = self._get_index_one()
        elif _type == '2':
            pass
        else:
            pass

        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), ret_res_json
        ).json()

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
from deploy.bo.menu import MenuBo
from deploy.bo.role import RoleBo
from deploy.bo.shortcut import ShortCutBo
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.config import ADMIN


MAX = 15


class DashboardService(object):
    """
    dashboard service
    """

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

    req_shortcut_attrs = [
        'rtx_id'
    ]

    req_shortcut_edit_attrs = [
        'rtx_id'
    ]

    req_shortcut_save_attrs = [
        'rtx_id',
        'select'
    ]

    def __init__(self):
        """
        dashboard service class initialize
        """
        self.sysuser_bo = SysUserBo()
        self.request_bo = RequestBo()
        self.menu_bo = MenuBo()
        self.role_bo = RoleBo()
        self.shortcut_bo = ShortCutBo()

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
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_pan_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
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
        click = self.request_bo.get_req_count_by_time(date_params)
        click = click[0] if click else 1
        if click == 0: click = 1        # 防止分母为0
        # <<<<<<<<<<<<<<<< get return pan: click >>>>>>>>>>>>>>>
        """ 本日操作数 / 总的API数量"""
        operate = self.request_bo.get_req_operate_by_time(date_params)
        operate = operate[0] if operate else 0
        ret_res_json = {
            'user': user,
            'click': click,
            'operate': round(operate/click * 100, 2)
        }
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), ret_res_json
        ).json()

    @staticmethod
    def _pan_chart_title(chart_type: str) -> str:
        """
        get dashboard pan chart title
        return string
        """
        if not chart_type:
            return "本周数据活跃情况"

        if chart_type == 'user':
            return '本周用户登录情况'
        elif chart_type == 'click':
            return '本周功能点击数情况'
        elif chart_type == 'operate':
            return '本周功能使用率情况'
        else:
            return "本周数据活跃情况"

    def pan_chart(self, params: dict) -> dict:
        """
        get dashboard pan chart data
        contain:
            - user 用户
            - click 点击率
            - operate 操作率
        """
        # ================= parameters check and format ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_pan_chart_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
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
            if k == 'type' and v not in ['user', 'click', 'operate']:
                return Status(
                    213, 'failure', u'请求参数%s值不合法' % k, {}).json()
            new_params[k] = str(v)
        # ---------------- parameter initialize ----------------
        rtx_id = new_params.get('rtx_id')
        _type = new_params.get('type')
        local_week = get_day_week_date(get_now_date())
        date_params = {
            "start_date": local_week.get('start_week_date'),
            "end_date": local_week.get('end_week_date')
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
            ret_res = self.request_bo.get_req_count_by_week(date_params) or []
        elif _type == 'operate':
            # <<<<<<<<<<<<<<<< get return operate 本周 >>>>>>>>>>>>>>>
            """总数"""
            ret_res_sum = self.request_bo.get_req_count_by_week(date_params) or []
            """数据操作数"""
            ret_res_count = self.request_bo.get_req_operate_count_by_week(date_params) or []
            ret_res = list()
            _temp_list = dict()
            # 把操作类型数据格式化为dict
            for _c in ret_res_count:
                if not _c: continue
                _temp_list[_c[0]] = _c[1]
            # 把对应日期的数据进行求率
            for _s in ret_res_sum:
                if not _s: continue
                v = _temp_list[_s[0]] if _s[0] in _temp_list.keys() else 0
                ret_res.append((_s[0], round(v/_s[1] * 100, 2)))
            del _temp_list
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
        for day in local_week.get('week_date'):   # 初始化数据，默认为0
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
        _ret_d = {
            'title': self._pan_chart_title(_type),
            'subtitle': '%s ~ %s' % (local_week.get('start_week_date'), local_week.get('end_week_date')),
            'data': list(_ret_week_dict.values())
        }
        return Status(
            100, 'success', StatusMsgs.get(100), _ret_d
        ).json()

    def _get_index_one(self):
        """
        指标1：系统功能累积使用情况
        """
        func_names = {
            'office.excel_merge': "表格合并",
            'office.excel_split': "表格拆分",
            'office.office_pdf_to': "PDF转WORD",
            'notify.dtalk_send': "钉钉绩效",
            'notify.qywx_send': "企微通知",
            'search.sqlbase_add': "SQL仓库"
        }
        # <<<<<<<<<<<<<<<<<< get all func rank >>>>>>>>>>>>>>>>>>>
        _res = self.request_bo.get_func_rank(params={'func_names': list(func_names.keys())})
        _ret_dict = OrderedDict()
        for key in func_names.keys():  # 初始化数据，默认为0
            if not key: continue
            _ret_dict[key] = 0
        """ ======== 在ret_res不为空情况下进行遍历 ======== """
        if _res:
            for _r in _res:  # 遍历每一个指定格式数据：date count
                if not _r: continue
                if _r and _r[0] not in func_names.keys(): continue
                _k = _r[0]
                _ret_dict[_k] = _r[1]   # 存在 && 更新
        _ret_res = list()
        for k, v in _ret_dict.items():
            if not k: continue
            _ret_res.append({"name": func_names.get(k), "value": v})
        _ret_data = {
            'data': _ret_res,
            'legend': list(func_names.values()),
            'title': '工具累积使用排名TOP%s' % len(func_names)
        }
        return _ret_data

    def _get_index_three(self):
        """
        指标3：本周API请求排行榜
        """
        # 不展示指标列表API
        no_show_endpoint = [
            'user.auth'
        ]
        # 最大展示指标数量
        SHOW_INDEX_MAX = 5
        api_endpoints = list()
        # 本周日期
        local_week = get_day_week_date(query_date=get_now(format="%Y-%m-%d"))
        params = {
            'start_time': '%s 00:00:00' % local_week.get('start_week_date'),
            'end_time': '%s 23:59:59' % local_week.get('end_week_date')
        }
        # <<<<<<<<<<<<<<<<<<<< get all func rank: 索取本周请求做多API>>>>>>>>>>>>>>>>>>>>>>
        api_res = self.request_bo.get_func_rank(params=params)
        start = 0
        for _d in api_res:
            """
            continue：
              - 无数据 
              - 指定api endpoint
              - dashboard.%
            """
            if not _d or _d[0] in no_show_endpoint \
                    or str(_d[0]).startswith('dashboard.'): continue
            api_endpoints.append(_d[0])
            start += 1
            if start >= SHOW_INDEX_MAX:
                break

        # <<<<<<<<<<<<<<<<<<<< 获取指定API本周次数 >>>>>>>>>>>>>>>>>>>>>>
        params['func_names'] = api_endpoints
        _res = self.request_bo.get_func_rank_group_by_api_date(params=params)
        _ret_dict = OrderedDict()
        for _d in api_endpoints:  # 初始化数据，默认为0
            if not _d: continue
            _ret_dict[_d] = [0, 0, 0, 0, 0, 0, 0]   # 本周数据初始化0
        """ ======== 在ret_res不为空情况下进行遍历 ======== """
        if _res:
            week_dates = local_week.get('week_date')     # 本周日期的列表，用于记录哪一天
            for _r in _res:  # 遍历每一个指定格式数据：date count
                if not _r: continue
                if _r[0] not in api_endpoints: continue
                index = week_dates.index(d2s(_r[1], fmt="%Y-%m-%d"))   # 记录索引，代表周一 ～ 周末 下角标
                try:
                    if index > 7: continue      # 不是本周的数据
                except:
                    continue
                _ret_dict[_r[0]][index] = _r[2]     # api endpoint -> date -> update
        _ret_list = list()
        for api in api_endpoints:
            if not api: continue
            _ret_list.append(_ret_dict.get(api))
        # 按API顺序加载
        _ret_res = {
            'data': _ret_list,
            'legend': api_endpoints,
            'title': '本周API请求次数排名TOP%s' % SHOW_INDEX_MAX,
            'subtitle': '%s ~ %s' % (local_week.get('start_week_date'), local_week.get('end_week_date'))
        }
        return _ret_res

    def index(self, params: dict) -> dict:
        """
        dashboard index chart data initialize
        指标数据 contain:
        index one 指标一：工具累积使用情况
        index two 指标二：
        index three 指标三：本周API请求排行榜
        """
        # ================= parameters check and format ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_index_chart_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
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
        elif _type == '3':
            ret_res_json = self._get_index_three()
        else:
            pass

        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), ret_res_json
        ).json()

    def shortcut(self, params: dict) -> dict:
        """
        dashboard short cut data
        :return: json data

        根据用户的角色权限，展示二级菜单快捷入口。
        思路：
        1.参数check and format
        2.获取全部菜单
        3.shortcut数据获取
        4.依据是否有shortcut数据进行情况判断
            4.1 有：直接格式化数据返回
            4.2 无：
                4.2.1 用户数据与用户权限数据check
                4.2.2 只取二级菜单 && 在权限id集合的菜单，如果shortcut为空，展示所有数据
        最多15个

        之所以这么做的原因在于如果设置了shortcut可以直接格式化数据进行返回，省去每次都需要判断用户、角色的情况
        """
        # ================= 1 - parameters check and format ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_shortcut_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_shortcut_attrs:     # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)

        # >>>>>>>>> 定义结果数据
        count = 0  # 最多展示15个快捷菜单
        ret_res_json = []
        rtx_id = new_params.get('rtx_id').strip()  # 去空格

        # -------------------- 2 - menu --------------------
        """目的是与二级菜单拼接"""
        _res = self.menu_bo.get_all(root=False)
        # 一级菜单【id-path】
        _one_level_menu = dict()
        for _r in _res:
            if not _r: continue
            if _r.level != 1: continue
            _one_level_menu[_r.id] = _r.path
        # -------------------- 3 - user shortcut --------------------
        shortcut = self.shortcut_bo.get_model_by_rtx(rtx_id)
        shortcut_list = list()
        if shortcut and shortcut.shortcut:
            shortcut_list = [int(x) for x in shortcut.shortcut.split(';') if x]
        # -------------------- 4 - 依据是否有shortcut数据进行情况判断 --------------------
        """ <<<<<<<<<<<<<<<<<<<<<<<<<<< 情况一 >>>>>>>>>>>>>>>>>>>>>>>>>>>"""
        if shortcut_list:
            for _r in _res:
                """ 过滤无数据/根节点/一级菜单/MENU不显示快捷入口"""
                if not _r: continue
                if _r.level != 2: continue  # 去掉根、一级菜单，只留二级菜单
                if not _r.is_shortcut: continue  # 去掉快捷入口设置不显示菜单
                if int(_r.id) in shortcut_list:
                    count += 1
                    ret_res_json.append({
                        'name': _r.title,
                        'icon': _r.icon,
                        'path': "%s/%s" % (_one_level_menu.get(_r.pid), _r.path)
                    })
                if count >= MAX:
                    break
            # return data
            return Status(
                100, 'success', StatusMsgs.get(100), ret_res_json).json()

        """ <<<<<<<<<<<<<<<<<<<<<<<<<<< 情况二 >>>>>>>>>>>>>>>>>>>>>>>>>>>"""
        # -------------------- 4.2.1 - check user and roles --------------------
        # get user by rtx
        user = self.sysuser_bo.get_auth_by_rtx(rtx_id)
        # user model is not exist
        if not user:
            return Status(
                202, 'failure', StatusMsgs.get(202) or u'用户未注册', {}).json()
        # user model is deleted
        if user.is_del:
            return Status(
                203, 'failure', StatusMsgs.get(203) or u'用户已注销', {}).json()
        # 判断是否管理员，如果是管理员是全部菜单权限
        # 多角色，if包含管理员，直接是管理员权限
        roles = str(user.role).split(';') if user.role else []  # 分割多角色
        is_admin = True if ADMIN in roles \
            else False
        auth_list = list()
        if not is_admin:
            # get authority by role list
            # user is admin, not get role, all authority menu
            role_models = self.role_bo.get_models_by_engnames(roles)
            for _r in role_models:
                if not _r or not _r.authority: continue
                auth_list.extend([int(x) for x in _r.authority.split(';') if x])
            auth_list = list(set(auth_list))  # 去重
            # auth_list.sort()   # 排序
        # --------------- 4.2.2.return legal data ---------------
        for _r in _res:
            """ 过滤无数据/根节点/一级菜单/MENU不显示快捷入口"""
            if not _r: continue
            if _r.level != 2: continue  # 去掉根、一级菜单，只留二级菜单
            if not _r.is_shortcut: continue  # 去掉快捷入口设置不显示菜单
            if is_admin:        # 具备管理员角色
                count += 1
                ret_res_json.append({
                    'name': _r.title,
                    'icon': _r.icon,
                    'path': "%s/%s" % (_one_level_menu.get(_r.pid), _r.path)
                })
            elif int(_r.id) in auth_list:    # 用户权限
                count += 1
                ret_res_json.append({
                    'name': _r.title,
                    'icon': _r.icon,
                    'path': "%s/%s" % (_one_level_menu.get(_r.pid), _r.path)
                })
            if count >= MAX:
                break
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), ret_res_json).json()

    def shortcut_edit(self, params: dict) -> dict:
        """
        dashboard short cut edit data list
        :return: json data

        1.参数检查 && 新参数格式化
        2.用户角色数据判断，获取角色权限数据
        3.shortcut数据
        4.全部菜单数据
        5.按shortcut数据进行分组，返回UnSelect【未选】，Select【已选】2组数据
        条件：在shortcut列表中 && 在角色权限中
        """
        # ================= 1 - parameters check and format ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_shortcut_edit_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_shortcut_edit_attrs:  # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:  # value is not null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)
        # -------------------- 2 - check user data and roles --------------------
        rtx_id = new_params.get('rtx_id').strip()  # 去空格
        # get user by rtx
        user = self.sysuser_bo.get_auth_by_rtx(rtx_id)
        # user model is not exist
        if not user:
            return Status(
                202, 'failure', StatusMsgs.get(202) or u'用户未注册', {}).json()
        # user model is deleted
        if user.is_del:
            return Status(
                203, 'failure', StatusMsgs.get(203) or u'用户已注销', {}).json()
        # 判断是否管理员，如果是管理员是全部菜单权限
        # 多角色，if包含管理员，直接是管理员权限
        roles = str(user.role).split(';') if user.role else []  # 分割多角色
        is_admin = True if ADMIN in roles \
            else False
        auth_list = list()
        if not is_admin:
            # get authority by role list
            # user is admin, not get role, all authority menu
            role_models = self.role_bo.get_models_by_engnames(roles)
            for _r in role_models:
                if not _r or not _r.authority: continue
                auth_list.extend([int(x) for x in _r.authority.split(';') if x])
            auth_list = list(set(auth_list))  # 去重
        # -------------------- 3 - user shortcut --------------------
        shortcut = self.shortcut_bo.get_model_by_rtx(rtx_id)
        shortcut_list = list()
        # 只有设置了shortcut才有数据
        if shortcut and shortcut.shortcut:
            shortcut_list = [int(x) for x in shortcut.shortcut.split(';') if x]
        # -------------------- 4 - menu --------------------
        """目的是与二级菜单拼接"""
        _res = self.menu_bo.get_all(root=False)
        # 一级菜单【只存储了id-title】
        _one_level_menu = dict()
        for _r in _res:
            if not _r: continue
            if _r.level != 1: continue
            _one_level_menu[_r.id] = _r.title or _r.name
        # --------------- 5.return UnSelect && Select ---------------
        select = list()
        unselect = list()
        # >>>>>>>>>>>>> 菜单数据过滤
        for _r in _res:
            """ 过滤无数据/根节点/一级菜单/MENU不显示快捷入口"""
            if not _r: continue
            if _r.level != 2: continue  # 去掉root、一级菜单，只留二级菜单
            if not _r.is_shortcut: continue  # 去掉menu快捷入口设置不显示菜单【管理员设置】
            """
            TODO: 加入一下角色权限判断
            菜单只有2种情况：
            1.select【已选】:
                数据加入select
            2.unselect【未选】
                2.1 如果是管理员，全部加入unselect
                2.2 如果非管理员，判断是否有role权限，如果有加入unselect
            """
            _d = {
                "id": _r.id,    # 菜单id
                "icon": _r.icon,    # 菜单图标
                "name": "%s > %s" % (_one_level_menu.get(_r.pid), _r.title or _r.name)  # 菜单路径：一级菜单 > 二级菜单
            }
            if int(_r.id) in shortcut_list:
                select.append(_d)
            else:
                if is_admin:  # 具备管理员角色
                    unselect.append(_d)
                elif not is_admin and int(_r.id) in auth_list:  # 用户设置权限
                    unselect.append(_d)
                else:   # 其他情况不加入
                    pass
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100),
            {"select": select, "unselect": unselect}
        ).json()

    def shortcut_save(self, params: dict) -> dict:
        """
        dashboard short cut edit data save
        :return: json data

        1.参数检查 && 格式化
        2.用户数据检查 && 角色权限
        3.快捷入口数据
            3.1 新增
            3.2 编辑
        """
        # ================= 1 - parameters check and format ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_shortcut_save_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_shortcut_save_attrs:  # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:  # value is not null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            if k == 'select':
                if not isinstance(v, list):     # select参数类型检查
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                if len(v) > 15:         # select参数长度检查，最大设置15个
                    return Status(
                        213, 'failure', u'超出设置上限，最多设置15个', {}).json()
                new_params[k] = ';'.join(v)  # 格式化成字符串存储
                new_params['select_list'] = v
            else:
                new_params[k] = str(v).strip()

        rtx_id = new_params.get('rtx_id').strip()  # 去空格
        # -------------------- 2 - check user and roles --------------------
        # get user by rtx
        user = self.sysuser_bo.get_auth_by_rtx(rtx_id)
        # user model is not exist
        if not user:
            return Status(
                202, 'failure', StatusMsgs.get(202) or u'用户未注册', {}).json()
        # user model is deleted
        if user.is_del:
            return Status(
                203, 'failure', StatusMsgs.get(203) or u'用户已注销', {}).json()
        # 判断是否管理员，如果是管理员是全部菜单权限
        # 多角色，if包含管理员，直接是管理员权限
        roles = str(user.role).split(';') if user.role else []  # 分割多角色
        is_admin = True if ADMIN in roles \
            else False
        auth_list = list()
        if not is_admin:
            # get authority by role list
            # user is admin, not get role, all authority menu
            role_models = self.role_bo.get_models_by_engnames(roles)
            for _r in role_models:
                if not _r or not _r.authority: continue
                auth_list.extend([int(x) for x in _r.authority.split(';') if x])
            auth_list = list(set(auth_list))  # 去重
            # >>>>>>>>> 加入一层角色权限判断，不在角色权限的去掉菜单ID
            new_select = list()
            for _mid in new_params.get('select_list'):
                if int(_mid) in auth_list:
                    new_select.append(_mid)
            new_params['select'] = ';'.join(new_select)
        # -------------------- 3 - shortcut model --------------------
        """
        2种情况：
        - 新增
        - 更新
        """
        shortcut = self.shortcut_bo.get_model_by_rtx(rtx_id)
        if not shortcut:        # 新增
            new_shortcut_model = self.shortcut_bo.new_mode()
            new_shortcut_model.rtx_id = rtx_id
            new_shortcut_model.shortcut = new_params['select']
            new_shortcut_model.create_time = get_now()
            new_shortcut_model.is_del = False
            self.shortcut_bo.add_model(new_shortcut_model)
        else:                   # 更新
            setattr(shortcut, 'shortcut', new_params['select'])
            setattr(shortcut, 'update_rtx', rtx_id)
            setattr(shortcut, 'update_time', get_now())
            self.shortcut_bo.merge_model(shortcut)
            # return data
        return Status(
            100, 'success', StatusMsgs.get(100), {}
        ).json()

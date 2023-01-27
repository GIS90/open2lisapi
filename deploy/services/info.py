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
import json
from operator import itemgetter
from itertools import groupby

from deploy.bo.enum import EnumBo
from deploy.bo.sysuser import SysUserBo
from deploy.bo.department import DepartmentBo
from deploy.bo.api import ApiBo
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import d2s, get_now, check_length, md5


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

    req_dict_disables_attrs = [
        'rtx_id',
        'list'
    ]

    req_delete_attrs = [
        'rtx_id',
        'md5'
    ]

    req_deletes_attrs = [
        'rtx_id',
        'list'
    ]

    req_detail_attrs = [
        'rtx_id',
        'md5'
    ]

    req_dict_update_attrs = [
        'rtx_id',
        'md5',
        # 'key',    # 禁用key更新字段
        'value',
        'status',
        'description',
        'order_id'
    ]

    req_dict_update_need_attrs = [
        'rtx_id',
        'md5',
        # 'key',    # 禁用key更新字段
        'value',
        'description'
    ]

    req_dict_update_check_len_attrs = {
        'rtx_id': 25,
        'name': 35,
        # 'key': 55,    # 禁用key更新字段
        'value': 55
    }

    req_dict_names_attrs = [
        'rtx_id'
    ]

    req_dict_add_attrs = [
        'rtx_id',
        'name',
        'key',
        'value',
        'description',
        'order_id',
        'type'
    ]

    req_dict_add_need_attrs = [
        'rtx_id',
        'name',
        'key',
        'value',
        'description',
        'type'
    ]

    req_dict_add_check_len_attrs = {
        'rtx_id': 25,
        'name': 35,
        'key': 55,
        'value': 55
    }

    req_depart_list_attrs = [
        'rtx_id'
    ]

    depart_list_attrs = [
        'id',
        'name',
        'md5_id',
        'description',
        'pid',
        'leaf',
        'lock',
        'dept_path',
        'deptid_path',
        'manage_rtx',
        'create_time',
        'create_rtx',
        'update_time',
        'update_rtx',
        'delete_time',
        'delete_rtx',
        'is_del',
        'order_id'
    ]

    api_list_attrs = [
        # 'id',
        'blueprint',
        'apiname',
        'endpoint',
        'md5_id',
        'path',
        'type',
        'short',
        'long',
        'create_time',
        'create_rtx',
        'delete_time',
        'delete_rtx',
        'update_time',
        'update_rtx',
        'is_del',
        'order_id'
    ]

    req_api_add_attrs = [
        'rtx_id',
        'blueprint',
        'apiname',
        'type',
        'short',
        'long',
        'order_id'
    ]

    req_api_add_need_attrs = [
        'rtx_id',
        'blueprint',
        'apiname',
        'type',
        'short',
        'long'
    ]

    req_api_add_ck_len_attrs = {
        'rtx_id': 25,
        'blueprint': 15,
        'apiname': 35,
        'type': 15,
        'short': 35,
        'long': 120
    }

    req_api_update_attrs = [
        'rtx_id',
        'blueprint',
        'apiname',
        'type',
        'short',
        'long',
        'order_id',
        'md5'
    ]

    req_api_types_attrs = [
        'rtx_id'
    ]

    def __init__(self):
        """
        information service class initialize
        """
        super(InfoService, self).__init__()
        self.DEPART_ROOT_ID = 1
        self.enum_bo = EnumBo()
        self.sysuser_bo = SysUserBo()
        self.depart_bo = DepartmentBo()
        self.api_bo = ApiBo()

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
                _res[attr] = getattr(model, 'name', '')
            elif attr == 'md5_id':
                _res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'key':
                _res[attr] = getattr(model, 'key', '')
            elif attr == 'value':
                _res[attr] = getattr(model, 'value', '')
            elif attr == 'description':
                _res[attr] = getattr(model, 'description', '')
            elif attr == 'status':
                _res[attr] = True if getattr(model, 'status') else False
            elif attr == 'create_rtx':
                _res[attr] = getattr(model, 'create_rtx', '')
            elif attr == 'create_time':
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'update_rtx':
                _res[attr] = getattr(model, 'update_rtx', '')
            elif attr == 'update_time':
                _res[attr] = self._transfer_time(model.update_time)
            elif attr == 'delete_rtx':
                _res[attr] = getattr(model, 'delete_rtx', '')
            elif attr == 'delete_time':
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'is_del':
                _res[attr] = model.is_del or False
            elif attr == 'order_id':
                _res[attr] = getattr(model, 'order_id', 1)
        else:
            return _res

    def _api_model_to_dict(self, model, _type='list'):
        """
        api model transfer to dict data
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.api_list_attrs:
            if not attr: continue
            if attr == 'id':
                _res[attr] = getattr(model, 'name', '')
            elif attr == 'blueprint':
                _res[attr] = getattr(model, 'blueprint', '')
            elif attr == 'apiname':
                _res[attr] = getattr(model, 'apiname', '')
            elif attr == 'endpoint':
                _res[attr] = getattr(model, 'endpoint', '')
            elif attr == 'md5_id':
                _res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'path':
                _res[attr] = getattr(model, 'path', '')
            elif attr == 'type':
                _res[attr] = getattr(model, 'type', '')
            elif attr == 'short':
                _res[attr] = getattr(model, 'short', '')
            elif attr == 'long':
                _res[attr] = getattr(model, 'long', '')
            elif attr == 'create_rtx':
                _res[attr] = getattr(model, 'create_rtx', '')
            elif attr == 'create_time':
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'update_rtx':
                _res[attr] = getattr(model, 'update_rtx', '')
            elif attr == 'update_time':
                _res[attr] = self._transfer_time(model.update_time)
            elif attr == 'delete_rtx':
                _res[attr] = getattr(model, 'delete_rtx', '')
            elif attr == 'delete_time':
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'is_del':
                _res[attr] = model.is_del or False
            elif attr == 'order_id':
                _res[attr] = getattr(model, 'order_id', 1)
        else:
            return _res

    def dict_list(self, params: dict) -> dict:
        """
        get dict data list by params
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
        # no data
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

        # ================= parameters check and format =================
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
        try:
            model.status = new_params.get('status')
            model.update_rtx = new_params.get('rtx_id')
            model.update_time = get_now()
            self.enum_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {'md5': new_params.get('md5')}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def dict_delete(self, params: dict) -> dict:
        """
        delete one dict data by md5
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
        try:
            setattr(model, 'is_del', True)
            setattr(model, 'delete_rtx', new_params.get('rtx_id'))
            setattr(model, 'delete_time', get_now())
            self.enum_bo.merge_model(model)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(322), {'md5': new_params.get('md5')}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def dict_deletes(self, params: dict) -> dict:
        """
        delete many dict data by md5 list
        params is dict
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # new format parameter
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_deletes_attrs:     # illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:   # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            if k == 'list':     # check type
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)
        # << batch delete >>
        try:
            res = self.enum_bo.batch_delete_by_md5(params=new_params)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(322), {'md5': new_params.get('md5')}).json()

        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def dict_disables(self, params: dict) -> dict:
        """
        batch many dict data status to False by md5 list
        params is dict
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # new format parameter
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_dict_disables_attrs:     # illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:   # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            if k == 'list':     # check type
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)
        # << batch disable >>
        try:
            res = self.enum_bo.batch_disable_by_md5(params=new_params)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {'md5': new_params.get('md5')}).json()

        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def dict_detail(self, params: dict):
        """
        get dict detail information by md5
        :return: json data
        """
        # ----------------- check and format --------------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_detail_attrs:  # illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>
        model = self.enum_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                302, 'failure', '数据已删除' or StatusMsgs.get(302), {}).json()
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), self._enum_model_to_dict(model, _type='detail')
        ).json()

    def dict_update(self, params: dict):
        """
        update dict data information by md5, contain:
            - key
            - value
            - description 描述
            - status 状态
            - order_id 排序ID
        :return: json data
        """
        # ----------------- check and format --------------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_dict_update_attrs:  # illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v and k in self.req_dict_update_need_attrs:  # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            if k == 'status' and not isinstance(v, bool):
                return Status(
                    213, 'failure', u'请求参数%s为Boolean类型' % k, {}).json()
            new_params[k] = v
        # 顺序ID特殊判断处理
        order_id = str(new_params.get('order_id'))
        if not order_id:
            new_params['order_id'] = 1
        if order_id and not order_id.isdigit():
            return Status(
                213, 'failure', u'请求参数order_id只允许为数字', {}).json()
        # parameters check length
        for _key, _value in self.req_dict_update_check_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # ========= check data
        model = self.enum_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}).json()
        # --------------------------------------- update model --------------------------------------
        try:
            # model.key = new_params.get('key')     # 禁用key更新
            model.value = new_params.get('value')
            model.description = new_params.get('description')
            model.status = new_params.get('status') or False    # 默认值False，非禁用状态
            model.order_id = new_params.get('order_id')   # 无order_id，默认值1
            self.enum_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {'md5': new_params.get('md5')}).json()
        
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def dict_names(self, params: dict):
        """
        get enum names list: key-value
        :return: json data
        """
        # ----------------- check and format --------------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_dict_names_attrs:  # illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>
        models = self.enum_bo.enum_group_by_name()
        # no data
        if not models:
            return Status(
                100, 'success', StatusMsgs.get(100), []).json()
        names = list()
        # 格式化
        for _m in models:
            if not _m: continue
            names.append({'label': _m[0], 'value': _m[0]})
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), names
        ).json()

    def dict_add(self, params: dict):
        """
        add enum model, contain:
            name
            key
            value
            desc
            order_id
            type
        :return: json data

        思路：
        1.参数校验
        2.新增/维护模式数据检查
        3.新增
        """
        # ----------------- check and format --------------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_dict_add_attrs:  # illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v and k in self.req_dict_add_need_attrs:       # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = v
        # 顺序ID特殊判断处理
        order_id = str(new_params.get('order_id'))
        if not order_id:
            new_params['order_id'] = 1
        if order_id and not order_id.isdigit():
            return Status(
                213, 'failure', u'请求参数order_id只允许为数字', {}).json()
        # type类型特殊检查【新增 && 维护】
        _type = new_params.get('type')
        if _type not in [1, 2, '1', '2']:
            return Status(
                213, 'failure', u'请求参数type不允许', {}).json()
        # parameters check length
        for _key, _value in self.req_dict_add_check_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # <<<<<<<<<<<<<<< 模型类型判断 >>>>>>>>>>>>>>>>>
        """
        类型：
            type=1：纯新增
            type=1：维护新增，已有name
        """
        _type = int(new_params.get('type'))
        models = self.enum_bo.get_add_model_by_name(name=new_params.get('name'))
        """ type=1：纯新增 校验name不允许存在 """
        if _type == 1 and models:
            return Status(
                301, 'failure', "枚举RTX已存在，请更换" or StatusMsgs.get(301), {}).json()
        """ type=2：维护新增 校验name需要存在 """
        if _type == 2 and not models:
            return Status(
                302, 'failure', "枚举RTX不存在，请重新选择" or StatusMsgs.get(301), {}).json()
        if _type == 2:
            _m = self.enum_bo.get_model_by_name_key(name=new_params.get('name'), key=new_params.get('key'))
            if _m:
                return Status(
                    301, 'failure', "数据已存在，请修改Key" or StatusMsgs.get(301), {}).json()
        """ md5 检验 """
        md5_id = md5('%s-%s-%s' % (new_params.get('name'), new_params.get('key'), get_now()))
        model_md5 = self.enum_bo.get_model_by_md5(md5_id)
        if model_md5:
            return Status(
                301, 'failure', "数据已存在，请更换MD5" or StatusMsgs.get(301), {}).json()
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< add model >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        try:
            new_model = self.enum_bo.new_mode()
            for attr in self.req_dict_add_attrs:
                if not attr or attr in ['rtx_id', 'type']: continue
                setattr(new_model, attr, new_params.get(attr))
            setattr(new_model, 'md5_id', md5_id)
            setattr(new_model, 'create_rtx', new_params.get('rtx_id'))
            setattr(new_model, 'create_time', get_now())
            setattr(new_model, 'is_del', False)     # 是否删除
            setattr(new_model, 'status', True)      # 状态
            self.enum_bo.add_model(new_model)
        except:
            return Status(
                320, 'failure', StatusMsgs.get(320), {'md5': md5_id}).json()
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': md5_id}
        ).json()

    def _depart_model_to_dict(self, model, _type='list'):
        """
        depart model transfer to dict data
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.depart_list_attrs:
            if not attr: continue
            if attr == 'id' and _type in ['list', 'tree']:
                _res[attr] = model.id
            elif attr == 'name' and _type in ['list', 'tree']:
                _res['label'] = model.name if getattr(model, 'name') else ""
            elif attr == 'md5_id' and _type in ['list', 'tree']:
                _res[attr] = model.md5_id if getattr(model, 'md5_id') else ""
            elif attr == 'description' and _type in ['list', 'tree']:
                _res[attr] = model.description if getattr(model, 'description') else ""
            elif attr == 'pid' and _type in ['list', 'tree']:
                _res[attr] = model.pid if getattr(model, 'pid') else ""
            elif attr == 'leaf' and _type in ['list', 'tree']:
                _res[attr] = True if getattr(model, 'leaf') else False
            elif attr == 'lock' and _type in ['list', 'tree']:
                _res[attr] = True if getattr(model, 'lock') else False
            elif attr == 'manage_rtx' and _type in ['list', 'tree']:
                _res[attr] = model.manage_rtx if getattr(model, 'manage_rtx') else ""
            elif attr == 'dept_path' and _type in ['list', 'tree']:
                _res[attr] = model.dept_path if getattr(model, 'dept_path') else ""
            elif attr == 'deptid_path' and _type in ['list', 'tree']:
                _res[attr] = model.deptid_path if getattr(model, 'deptid_path') else ""
            elif attr == 'create_rtx' and _type in ['list']:
                _res[attr] = model.create_rtx if getattr(model, 'create_rtx') else ""
            elif attr == 'create_time' and _type in ['list']:
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'update_rtx' and _type in ['list']:
                _res[attr] = model.update_rtx if getattr(model, 'update_rtx') else ""
            elif attr == 'update_time' and _type in ['list']:
                _res[attr] = self._transfer_time(model.update_time)
            elif attr == 'delete_rtx' and _type in ['list']:
                _res[attr] = model.delete_rtx if getattr(model, 'delete_rtx') else ""
            elif attr == 'delete_time' and _type in ['list']:
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'is_del' and _type in ['list']:
                _res[attr] = True if getattr(model, 'is_del') else False
            elif attr == 'order_id' and _type in ['list', 'tree']:
                _res[attr] = model.order_id if getattr(model, 'order_id') else 1
        else:
            return _res

    def _search_child_fab(self, node_id, all_nodes):
        if not node_id or not all_nodes:
            return []
        all_nodes.sort(key=itemgetter('pid'))
        for key, group in groupby(all_nodes, key=itemgetter('pid')):
            if node_id == key:
                return self._search_child_fab(self, key, group)
        else:
            return 

    def _nodes_fab(self, root_direct_child_ids, all_nodes):
        if not all_nodes:
            return []
        all_nodes.sort(key=itemgetter('pid'))
        _res = dict()
        for node_id in root_direct_child_ids:
            if not node_id: continue        # no node id
            _res[node_id] = self._search_child_fab(node_id, all_nodes)
        else:
            return _res

    def depart_list(self, params: dict) -> dict:
        """
        get department data list by params
        params is dict
        return json data

        https://element.eleme.cn/2.13/#/zh-CN/component/tree
        节点属性：
        id：ID值
        name：部门名称
        md5_id：数据记录record
        description：部门描述
        pid：上级部门ID
        leaf：是否为叶子节点，如果为True不允许有子节点，默认为False
        lock：是否锁定，如果为True为锁定，默认为False
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        """
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_depart_list_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            new_params[k] = str(v).strip()

        rtx_id = new_params.get('rtx_id')
        user_model = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        if not user_model:
            return Status(
                302, 'failure', u'用户%s不存在' % rtx_id, {}).json()
        # **************** <get data> *****************
        res = self.depart_bo.get_all(root=True)
        # no data
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # <<<<<<<<<<<<<<<<<<<< format and return data >>>>>>>>>>>>>>>>>>>>
        new_res_dict = dict()   # 所有节点信息：{ 节点id: 节点, 节点id: 节点 }
        all_nodes = list()   # 根所有所有的children节点信息：[{ id: id, name: name },{ id: id, name: name } ]
        root_direct_child_nodes = list()     # root节点的直属children
        for _d in res:
            # filter no id or no parent id
            if not _d or not getattr(_d, 'id'):continue
            _res_dict = self._depart_model_to_dict(_d, _type='tree')
            if _res_dict:
                new_res_dict[_res_dict.get('id')] = _res_dict
                if _res_dict.get('id') != self.DEPART_ROOT_ID:
                    all_nodes.append(_res_dict)
                # 获取root节点下的所有子节点
                if _res_dict.get('pid') == self.DEPART_ROOT_ID:
                    root_direct_child_nodes.append(_res_dict)
        ret_res = list()  # return result, list type
        root_direct_child_nodes_ids = [node.get('id') for node in root_direct_child_nodes if node.get('id')]
        nodes_fab = self._nodes_fab(root_direct_child_nodes_ids, all_nodes)
        # 分2种情况：有root节点 无root节点
        if new_res_dict.get(self.DEPART_ROOT_ID):
            root = new_res_dict.get(self.DEPART_ROOT_ID)
            root['children'] = root_direct_child_nodes
            ret_res.append(root)
        else:
            ret_res = root_direct_child_nodes
        print(ret_res)
        """
        return Status(
            100, 'success', StatusMsgs.get(100), []
        ).json()

    def depart_update(self, params: dict) -> dict:
        """
        information > update department information
        :return: json data
        """
        return Status(
            100, 'success', StatusMsgs.get(100), {}
        ).json()

    def api_list(self, params: dict) -> dict:
        """
        get api list from api table by params
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
        res, total = self.api_bo.get_all(new_params)
        # no data
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # <<<<<<<<<<<<<<<<<<<< format and return data >>>>>>>>>>>>>>>>>>>>
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._api_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def api_delete(self, params: dict) -> dict:
        """
        delete one api data by md5
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
        model = self.api_bo.get_model_by_md5(md5_id=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}).json()
        # < update data >
        try:
            setattr(model, 'is_del', True)
            setattr(model, 'delete_rtx', new_params.get('rtx_id'))
            setattr(model, 'delete_time', get_now())
            self.api_bo.merge_model(model)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {'md5': new_params.get('md5')}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def api_deletes(self, params: dict) -> dict:
        """
        delete many api data by md5 list
        params is dict
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # new format parameter
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_deletes_attrs:     # illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:   # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            if k == 'list':     # check type
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)
        # << batch delete >>
        try:
            res = self.api_bo.batch_delete_by_md5(params=new_params)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {'md5': new_params.get('md5')}).json()
        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def api_detail(self, params: dict) -> json:
        """
        get api detail information by md5
        :return: json data
        """
        # ----------------- check and format --------------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_detail_attrs:  # illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>
        model = self.api_bo.get_model_by_md5(md5_id=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                302, 'failure', '数据已删除' or StatusMsgs.get(302), {}).json()
        # -------------- return data -----------------
        # type list
        type_models = self.enum_bo.get_model_by_name(name='api-type')
        _type_res = list()
        # not exist
        for _m in type_models:
            if not _m: continue
            _type_res.append({'key': _m.key, 'value': _m.value})
        # detail
        _res = {
            'detail': self._api_model_to_dict(model, _type='detail'),
            'type': _type_res
        }
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), _res
        ).json()

    def api_add(self, params: dict):
        """
        add api model, contain:
            - blueprint
            - apiname
            - type
            - short
            - long
            - order_id
        其中:
            - endpoint = blueprint.apiname
            - path = /blueprint/apiname
        :return: json data

        思路：
        1.参数校验
        2.新增
        """
        # ----------------- check and format --------------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_api_add_attrs:  # illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v and k in self.req_api_add_need_attrs:       # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = v
        # 顺序ID特殊判断处理
        order_id = str(new_params.get('order_id'))
        if not order_id:
            new_params['order_id'] = 1
        if order_id and not order_id.isdigit():
            return Status(
                213, 'failure', u'请求参数order_id只允许为数字', {}).json()
        # parameters check length
        for _key, _value in self.req_api_add_ck_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # <<<<<<<<<<<<<<< md5模型判断 >>>>>>>>>>>>>>>>>
        md5_id = md5('%s-%s' % (new_params.get('blueprint'), new_params.get('apiname')))
        model_md5 = self.api_bo.get_model_by_md5(md5_id)
        if model_md5:
            return Status(
                301, 'failure', "数据已存在" or StatusMsgs.get(301), {}).json()
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< add model >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        try:
            new_model = self.api_bo.new_mode()
            for _k, _v in new_params.items():
                if _k in ['rtx_id']:
                    setattr(new_model, 'create_rtx', _v)
                    setattr(new_model, 'update_rtx', _v)
                else:
                    setattr(new_model, _k, _v)
            setattr(new_model, 'md5_id', md5_id)
            """ 
            - endpoint = blueprint.apiname
            - path = /blueprint/apiname
            """
            setattr(new_model, 'endpoint', '%s.%s' % (new_params.get('blueprint'), new_params.get('apiname')))
            setattr(new_model, 'path', '/%s/%s' % (new_params.get('blueprint'), new_params.get('apiname')))
            setattr(new_model, 'create_time', get_now())
            setattr(new_model, 'update_time', get_now())
            setattr(new_model, 'is_del', False)     # 是否删除
            self.api_bo.add_model(new_model)
        except:
            return Status(
                320, 'failure', StatusMsgs.get(320), {'md5': new_params.get('md5')}).json()
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': md5_id}).json()

    def api_update(self, params: dict):
        """
        update the exist api model, contain:
            - blueprint
            - apiname
            - type
            - short
            - long
            - order_id
        其中:
            - endpoint = blueprint.apiname
            - path = /blueprint/apiname
        :return: json data
        """
        # ----------------- check and format --------------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_api_update_attrs:  # illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v and k in self.req_api_add_need_attrs:       # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = v
        # 顺序ID特殊判断处理
        order_id = str(new_params.get('order_id'))
        if not order_id:
            new_params['order_id'] = 1
        if order_id and not order_id.isdigit():
            return Status(
                213, 'failure', u'请求参数order_id只允许为数字', {}).json()
        # parameters check length
        for _key, _value in self.req_api_add_ck_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # <<<<<<<<<<<<<<< check data >>>>>>>>>>>>>>>>>
        model = self.api_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}).json()
        # --------------------------------------- update model --------------------------------------
        rtx_id = new_params.get('rtx_id')
        new_params.pop('rtx_id')
        new_params.pop('md5')
        try:
            for _k, _v in new_params.items():
                setattr(model, _k, _v)
            """ 
            - endpoint = blueprint.apiname
            - path = /blueprint/apiname
            """
            setattr(model, 'endpoint', '%s.%s' % (new_params.get('blueprint'), new_params.get('apiname')))
            setattr(model, 'path', '/%s/%s' % (new_params.get('blueprint'), new_params.get('apiname')))
            setattr(model, 'update_time', get_now())
            setattr(model, 'update_rtx', rtx_id)
            self.api_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {'md5': new_params.get('md5')}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def api_types(self, params: dict):
        """
        get api type list: key-value
        :return: json data
        """
        # ----------------- check and format --------------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_api_types_attrs:  # illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>
        models = self.enum_bo.get_model_by_name(name='api-type')
        # no data
        if not models:
            return Status(
                100, 'success', StatusMsgs.get(100), []).json()
        _res = list()
        # 格式化
        for _m in models:
            if not _m: continue
            _res.append({'key': _m.key, 'value': _m.value})
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), _res).json()

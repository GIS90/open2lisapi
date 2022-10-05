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
        'key',
        'value',
        'status',
        'description',
        'order_id'
    ]

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
                _res[attr] = model.md5_id if getattr(model, 'md5_id') else ""
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
        model.status = new_params.get('status')
        model.update_rtx = new_params.get('rtx_id')
        model.update_time = get_now()
        self.enum_bo.merge_model(model)
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
        setattr(model, 'is_del', True)
        setattr(model, 'delete_rtx', new_params.get('rtx_id'))
        setattr(model, 'delete_time', get_now())
        self.enum_bo.merge_model(model)
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
        res = self.enum_bo.batch_delete_by_md5(params=new_params)
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
        res = self.enum_bo.batch_disable_by_md5(params=new_params)
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
        # ==================== check parameters ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_dict_update_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in ['order_id', 'status']:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            # check: length
            if k == 'key' and not check_length(v, 25):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'value' and not check_length(v, 55):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'description' and not check_length(v, 255):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'status' and not isinstance(v, bool):
                return Status(
                    213, 'failure', u'请求参数%s为Boolean类型' % k, {}).json()
            elif k == 'order_id':  # 顺序ID特殊判断处理
                if v and not str(v).isdigit():
                    return Status(
                        213, 'failure', u'请求参数%s只允许为数字' % k, {}).json()
                v = int(v) if v else 1  # 默认order_id：1
            new_params[k] = str(v) if k not in ['order_id', 'status'] else v

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
        model.key = new_params.get('key')
        model.value = new_params.get('value')
        model.description = new_params.get('description')
        model.status = new_params.get('status') or False    # 默认值False，非禁用状态
        model.order_id = new_params.get('order_id')   # 无order_id，默认值1
        self.enum_bo.merge_model(model)
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
        # not exist
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
            if not v and k not in ['order_id', 'status']:       # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            # check: length
            if k == 'name' and not check_length(v, 25):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'key' and not check_length(v, 25):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'value' and not check_length(v, 55):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'description' and not check_length(v, 255):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'status' and not isinstance(v, bool):
                return Status(
                    213, 'failure', u'请求参数%s为Boolean类型' % k, {}).json()
            elif k == 'type' and v not in [1, 2, '1', '2']:     # type类型特殊检查
                return Status(
                    213, 'failure', u'请求参数%s不允许' % k, {}).json()
            elif k == 'order_id':  # 顺序ID特殊判断处理
                if v and not str(v).isdigit():
                    return Status(
                        213, 'failure', u'请求参数%s只允许为数字' % k, {}).json()
                v = int(v) if v else 1  # 默认order_id：1
            new_params[k] = str(v) if k not in ['order_id', 'status'] else v
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
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': md5_id}
        ).json()

    def depart_list(self, params: dict) -> dict:
        """
        get department data list by params
        params is dict
        return json data

        https://github.com/ParadeTo/vue-tree-list
        节点属性：
        name                    type            default	            description
        ------------------------------------------------------------------------------------------
        id                      string, number  current timestamp   The node's id
        isLeaf                  boolean         false               The node is leaf or not
        dragDisabled            boolean         false               Forbid dragging tree node
        addTreeNodeDisabled	    boolean         false               Show addTreeNode button or not
        addLeafNodeDisabled	    boolean         false               Show addLeafNode button or not
        editNodeDisabled        boolean         false               Show editNode button or not
        delNodeDisabled	        boolean         false               Show delNode button or not
        children                array           null                The children of node

        """
        _res = [
            {
              "name": 'Node 1',
              "id": 1,
              "pid": 0,
              "isLeaf": False,
              "disabled": False,
              "dragDisabled": False,
              "addTreeNodeDisabled": False,
              "addLeafNodeDisabled": False,
              "editNodeDisabled": False,
              "delNodeDisabled": False,
              "children": [
                {
                  "name": 'Node 1-1',
                  "id": 11,
                  "pid": 1
                },
                {
                  "name": 'Node 1-2',
                  "id": 12,
                  "pid": 1
                }
              ]
            },
            {
              "name": 'Node 2',
              "id": 2,
              "pid": 0
            },
            {
              "name": 'Node 3',
              "id": 3,
              "pid": 0
            }
        ]
        return Status(
            100, 'success', StatusMsgs.get(100), _res
        ).json()
        # # ====================== parameters check ======================
        # if not params:
        #     return Status(
        #         212, 'failure', StatusMsgs.get(212), {}).json()
        # # new parameters
        # new_params = dict()
        # for k, v in params.items():
        #     if not k: continue
        #     if k not in self.req_dict_list_attrs and v:
        #         return Status(
        #             213, 'failure', u'请求参数%s不合法' % k, {}).json()
        #     if k == 'limit':
        #         v = int(v) if v else self.PAGE_LIMIT
        #     elif k == 'offset':
        #         v = int(v) if v else 0
        #     else:
        #         v = str(v) if v else ''
        #     new_params[k] = v
        #
        # # **************** <get data> *****************
        # res, total = self.enum_bo.get_all(new_params)
        # # no data
        # if not res:
        #     return Status(
        #         101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # # <<<<<<<<<<<<<<<<<<<< format and return data >>>>>>>>>>>>>>>>>>>>
        # new_res = list()
        # n = 1
        # for _d in res:
        #     if not _d: continue
        #     _res_dict = self._enum_model_to_dict(_d)
        #     if _res_dict:
        #         _res_dict['id'] = n
        #         new_res.append(_res_dict)
        #         n += 1
        # return Status(
        #     100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        # ).json()

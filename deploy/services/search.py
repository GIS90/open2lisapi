# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/12/21 18:24"
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
# usage: /usr/bin/python search.py
# ------------------------------------------------------------
import json

from deploy.bo.sqlbase import SqlbaseBo
from deploy.bo.sysuser import SysUserBo
from deploy.bo.enum import EnumBo

from deploy.config import OFFICE_LIMIT, ADMIN, ADMIN_AUTH_LIST
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import d2s, get_now, md5, check_length, s2d


class SearchService(object):
    """
    search service
    """

    SHOW_TEXT_MAX = 55

    req_sqlbase_list_attrs = [
        'rtx_id',   # 查询用户rtx
        'limit',    # 条数
        'offset',   # 偏移多少条
        'public',
        'create_time_start',    # 起始创建时间
        'create_time_end',  # 结束创建时间
        'create_rtx',   # 创建用户RTX
        'author',   # 作者（定义数组，支持多选）
        'public_time_start',     # 起始发布时间
        'public_time_end',  # 结束发布时间
        'recommend',     # 推荐度
        'database',     # 数据库类型
        'label',     # 标签
        'content',  # 内容
        'count_start',  # 浏览次数上限
        'count_end'     # 浏览次数下限
    ]

    req_sqlbase_list_search_list_types = [
        'create_rtx',
        'author',
        'recommend',
        'database',
        'label'
    ]

    req_sqlbase_list_search_int_types = [
        'count_start',
        'count_end'
    ]

    req_sqlbase_list_search_time_types = [
        'create_time_start',  # 起始创建时间
        'create_time_end',  # 结束创建时间
        'public_time_start',  # 起始发布时间
        'public_time_end'  # 结束发布时间
    ]

    req_sqlbase_list_search_like_types = [
        'content'
    ]

    sqlbase_list_attrs = [
        # 'id',
        'rtx_id',
        'title',
        'md5_id',
        'author',
        'recommend',
        'summary',
        'database',
        'public',
        'public_time',
        'html',
        'text',
        'count',
        'create_time',
        'delete_rtx',
        'delete_time',
        'is_del'
    ]

    req_sqlbase_add_attrs = [
        'rtx_id',
        'title',
        'author',
        'recommend',
        'database',
        'summary',
        'label',
        'public',
        'public_time',
        'html',
        'text'
    ]

    req_add_init_attrs = [
        'rtx_id'
    ]

    req_sqlbase_edit_no_need_attrs = [
        'summary',
        'label'
    ]

    req_sqlbase_edit_ck_len_attrs = {
        'rtx_id': 25,
        'title': 55,
        'author': 25,
        'summary': 200
    }

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
        'md5',
        'type'
    ]

    req_sqlbase_update_attrs = [
        'rtx_id',
        'title',
        'author',
        'recommend',
        'database',
        'summary',
        'label',
        'public_time',
        'html',
        'text',
        'md5'
    ]

    def __init__(self):
        """
        search service class initialize
        """
        self.sqlbase_bo = SqlbaseBo()
        self.sysuser_bo = SysUserBo()
        self.enum_bo = EnumBo()

    def _transfer_time(self, t):
        if not t:
            return ""

        if not isinstance(t, str):
            return d2s(t)
        elif isinstance(t, str) and t == '0000-00-00 00:00:00':
            return ""
        else:
            return t or ''

    def _sqlbase_model_to_dict(self, model, _type='list') -> dict:
        """
        sqlbase model object transfer to dict type
        """
        if not model:
            return {}
        _res = dict()
        for attr in self.sqlbase_list_attrs:
            if not attr: continue
            if attr == 'id':
                _res[attr] = getattr(model, 'id', '')
            elif attr == 'rtx_id':
                _res[attr] = getattr(model, 'rtx_id', '')
            elif attr == 'title':
                _res[attr] = getattr(model, 'title', '')
            elif attr == 'md5_id':
                _res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'author':
                _res[attr] = getattr(model, 'author', '')
            elif attr == 'recommend':
                _res[attr] = getattr(model, 'recommend', '')
            elif attr == 'database':
                _res[attr] = getattr(model, 'database', '')
            elif attr == 'summary':
                _res[attr] = getattr(model, 'summary', '')
            elif attr == 'public':
                _res[attr] = getattr(model, 'public', '')
            elif attr == 'public_time':
                _res[attr] = self._transfer_time(model.public_time)
            elif attr == 'html' and _type == 'detail':
                _res[attr] = getattr(model, 'html', '')
            elif attr == 'text':
                text = getattr(model, 'text', '')
                if text and _type == 'list' and len(text) > self.SHOW_TEXT_MAX:
                    # 加了展示字数的限制，否则页面展示太多
                    text = '%s...具体内容请查看详情' % text[0:self.SHOW_TEXT_MAX]
                _res[attr] = text
            elif attr == 'count':
                _res[attr] = getattr(model, 'count', 0)
            elif attr == 'create_time':
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'delete_rtx':
                _res[attr] = getattr(model, 'delete_rtx', '')
            elif attr == 'delete_time':
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'is_del':
                _res[attr] = True if model.is_del else False
        else:
            return _res

    def sqlbase_list(self, params: dict) -> json:
        """
        get sqlbase list by params
        params is dict
        return json data
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_sqlbase_list_attrs and v:  # is illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if k in self.req_sqlbase_list_search_list_types:    # 处理列表参数
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s为列表类型' % k, {}).json()
            if k in self.req_sqlbase_list_search_time_types and v:      # 处理时间查询参数，str类型
                if not isinstance(v, str):
                    return Status(
                        213, 'failure', u'请求参数%s为字符串类型' % k, {}).json()
                if v:
                    try:
                        s2d(v)
                    except:
                        return Status(
                            213, 'failure', u'请求参数%s格式：yyyy-MM-dd HH:mm:ss' % k, {}).json()
            if k in self.req_sqlbase_list_search_like_types and v:      # like 查询参数
                v = '%' + str(v) + '%'
            if k in self.req_sqlbase_list_search_int_types and v:      # int类型查询参数
                if not str(v).isdigit():
                    return Status(
                        213, 'failure', u'请求参数%s为数字类型' % k, {}).json()
                v = int(v)
            elif k == 'limit':
                v = int(v) if v else OFFICE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            elif k == 'public':
                v = True if v else False
            # 参数写入new-params
            new_params[k] = v

        # **************** 全员获取ALL数据 *****************
        req_rtx_id = new_params.get('rtx_id')
        new_params.pop('rtx_id')
        # <get data>
        res, total = self.sqlbase_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # ////////////////// return data \\\\\\\\\\\\\\\\\\\\\
        """ sqlbase list """
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._sqlbase_model_to_dict(_d, _type='list')
            if _res_dict:
                _res_dict['id'] = n
                _res_dict['edit'] = 'true' if req_rtx_id in [_res_dict.get('rtx_id'), ADMIN] else 'false'
                new_res.append(_res_dict)
                n += 1
        """ all user k-v list"""
        user_res, _ = self.sysuser_bo.get_all(new_params, is_admin=True, is_del=True)
        user_list = list()
        for _d in user_res:
            if not _d: continue
            user_list.append({'key': _d.rtx_id, 'value': _d.fullname})
        # all database type
        database_res = self.enum_bo.get_model_by_name(name='db-type')
        database_list = list()
        for _d in database_res:
            if not _d: continue
            database_list.append({'key': _d.key, 'value': _d.value})
        return Status(
            100, 'success', StatusMsgs.get(100),
            {
                'list': new_res,
                'total': total,
                'user': user_list,
                'database': database_list
            }
        ).json()

    def sqlbase_add(self, params: dict) -> dict:
        """
        add new data to db table sqlbase, new data is dict object
        :return: json data
        """
        # ===== check parameters && format parameters ======
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_sqlbase_add_attrs:
                return Status(
                    213, 'failure', '请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in self.req_sqlbase_edit_no_need_attrs:  # is not null
                return Status(
                    214, 'failure', '请求参数%s为必须信息' % k, {}).json()
            new_params[k] = v
        # parameters length check
        for _key, _value in self.req_sqlbase_edit_ck_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()
        try:
            # create new model
            new_model = self.sqlbase_bo.new_mode()
            # 默认值
            new_params['md5_id'] = md5(new_params.get('title')+get_now()+new_params.get('rtx_id'))
            new_params['create_time'] = get_now()
            new_params['is_del'] = False
            new_params['count'] = 0
            for key, value in new_params.items():
                if not key: continue
                setattr(new_model, key, value)
            else:
                self.sqlbase_bo.add_model(new_model)
        except:
            return Status(
                320, 'failure', StatusMsgs.get(320), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {}).json()

    def sqlbase_add_init(self, params: dict) -> json:
        """
        sql data enum list
        :return: json data
        """
        # ================== parameters check && format ==================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_add_init_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)

        # <<<<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>>>>
        # all users
        user_res, _ = self.sysuser_bo.get_all(new_params, is_admin=True, is_del=True)
        user_list = list()
        for _d in user_res:
            if not _d: continue
            user_list.append({'key': _d.rtx_id, 'value': _d.fullname})
        # all database type
        database_res = self.enum_bo.get_model_by_name(name='db-type')
        database_list = list()
        for _d in database_res:
            if not _d: continue
            database_list.append({'key': _d.key, 'value': _d.value})
        _res = {
            'user': user_list,
            'database': database_list
        }
        return Status(
            100, 'success', StatusMsgs.get(100), _res).json()

    def sqlbase_delete(self, params: dict) -> json:
        """
        delete one sqlbase data by params
        params is dict
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

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
        model = self.sqlbase_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        ADMIN_AUTH_LIST.extend([ADMIN, model.rtx_id])
        if rtx_id not in ADMIN_AUTH_LIST:
            return Status(
                311, 'failure', StatusMsgs.get(311), {}).json()
        # <update data> 软删除
        try:
            model.is_del = True
            model.delete_rtx = rtx_id
            model.delete_time = get_now()
            self.sqlbase_bo.merge_model(model)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def sqlbase_deletes(self, params: dict) -> json:
        """
        delete many sqlbase data by params
        params is dict
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_deletes_attrs:
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
        # **************** 管理员获取ALL数据 *****************
        ADMIN_AUTH_LIST.extend([ADMIN])     # 特权账号
        if new_params.get('rtx_id') in ADMIN_AUTH_LIST:
            new_params.pop('rtx_id')
        # << batch delete >>
        try:
            res = self.sqlbase_bo.batch_delete_by_md5(params=new_params)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()
        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def sqlbase_detail(self, params: dict) -> json:
        """
        get the latest sqlbase detail information by md5
        :return: json data
        """
        # ================== parameters check && format ==================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_detail_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        _type = new_params.get('type')
        if _type not in ['edit', 'view']:
            return Status(
                213, 'failure', u'请求参数type不合法', {}).json()
        # <<<<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>>>>
        model = self.sqlbase_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                302, 'failure', '数据已删除' or StatusMsgs.get(302), {}).json()
        # authority【管理员具有所有数据权限】
        # rtx_id = new_params.get('rtx_id')
        # if rtx_id not in [ADMIN, model.rtx_id]:
        #     return Status(
        #         309, 'failure', StatusMsgs.get(309), {}).json()
        """  return data """
        # all users
        user_res, _ = self.sysuser_bo.get_all(new_params, is_admin=True, is_del=True)
        user_list = list()
        for _d in user_res:
            if not _d: continue
            user_list.append({'key': _d.rtx_id, 'value': _d.fullname})
        # all database type
        database_res = self.enum_bo.get_model_by_name(name='db-type')
        database_list = list()
        for _d in database_res:
            if not _d: continue
            database_list.append({'key': _d.key, 'value': _d.value})
        _res = {
            'user': user_list,
            'database': database_list,
            'detail': self._sqlbase_model_to_dict(model, _type='detail')
        }
        """ 浏览文章增加次数 """
        if _type == 'view':
            try:
                setattr(model, 'count', model.count + 1)
                self.sqlbase_bo.merge_model(model)
            except:
                pass
        return Status(
            100, 'success', StatusMsgs.get(100), _res).json()

    def sqlbase_update(self, params: dict) -> json:
        """
        update sqlbase message information, contain:
            - title 标题
            - html/text 内容
            - author 作者
            - public—time 发布时间
            - recommend 推荐度
            - summary 简述
            - label 标签
        by data md5
        :return: json data
        """
        # ====================== parameters check and format ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_sqlbase_update_attrs and v:      # 不合法参数
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in self.req_sqlbase_edit_no_need_attrs:  # is not null
                return Status(
                    214, 'failure', '请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
            # check: length
        for _key, _value in self.req_sqlbase_edit_ck_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # <<<<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>>>>
        model = self.sqlbase_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                302, 'failure', '数据已删除' or StatusMsgs.get(302), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        ADMIN_AUTH_LIST.extend([ADMIN, model.rtx_id])
        if rtx_id not in ADMIN_AUTH_LIST:
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()

        # --------------------------------------- update model --------------------------------------
        for key, value in new_params.items():
            if not key: continue
            setattr(model, key, value)
        try:
            self.sqlbase_bo.merge_model(model)
            return Status(
                100, 'success', StatusMsgs.get(100), {'md5': model.md5_id}).json()
        except:
            return Status(
                450, 'failure', StatusMsgs.get(450), {'md5': model.md5_id}).json()

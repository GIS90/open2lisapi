# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    search service

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
import datetime
from collections import OrderedDict

from deploy.bo.sqlbase import SqlbaseBo
from deploy.bo.sysuser import SysUserBo
from deploy.bo.enum import EnumBo

from deploy.config import OFFICE_LIMIT
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.utils import d2s, get_now, md5, check_length, s2d, auth_rtx_join


class SearchService(object):
    """
    search service
    """

    SHOW_TEXT_MAX = 55

    # 用户
    req_user_necessary_attrs = ['rtx_id']

    # 数据md5
    req_md5_necessary_attrs = ['rtx_id', 'md5']

    # define many request api parameters
    # 分页数据通用请求参数
    req_page_comm_attrs = [
        'rtx_id',
        'limit',
        'offset'
    ]

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
        'is_del',
        'enum_value'
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

    req_sqlbase_no_update_attrs = [
        'rtx_id',
        'md5'
    ]

    req_share_list_attrs = [
        'rtx_id',   # 查询用户rtx
        'limit',    # 条数
        'offset',   # 偏移多少条
        'create_time_start',    # 起始创建时间
        'create_time_end',  # 结束创建时间
        'create_rtx',   # 创建用户RTX
        'content'    # 模糊查询内容
    ]

    req_share_list_search_like_types = [
        'search'  # 模糊查询内容
    ]

    req_share_list_search_list_types = [
        'create_rtx'
    ]

    req_share_list_search_int_types = [
        'count_start',
        'count_end'
    ]

    req_share_list_search_time_types = [
        'create_time_start',  # 起始创建时间
        'create_time_end',  # 结束创建时间
        # 'public_time_start',  # 起始发布时间
        # 'public_time_end'  # 结束发布时间
    ]

    def __init__(self):
        """
        SearchService class initialize
        """
        super(SearchService, self).__init__()
        # bo
        self.sqlbase_bo = SqlbaseBo()
        self.sysuser_bo = SysUserBo()
        self.enum_bo = EnumBo()

    def __str__(self):
        print("SearchService class.")

    def __repr__(self):
        self.__str__()

    def _transfer_time(self, t):
        """
        数据库datetime字段 TO 字符串格式时间字段
        """
        if not t:
            return ""

        if isinstance(t, datetime.datetime):
            return d2s(t)
        elif isinstance(t, str) and t == '0000-00-00 00:00:00':
            return ""
        else:
            return t or ''

    def _sqlbase_model_to_dict(self, model, _type='list') -> dict:
        """
        sqlbase model object transfer to dict type

        list：数据列表
        detail：数据详情
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
            elif attr == 'html' and _type in ['detail']:
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
            elif attr == 'enum_value':
                _res['database_value'] = getattr(model, 'enum_value', '')
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
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_page_comm_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_sqlbase_list_attrs and v:  # is illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k or StatusMsgs.get(213), {}).json()
            if k in self.req_sqlbase_list_search_list_types:    # 处理列表参数
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s为列表类型' % k or StatusMsgs.get(213), {}).json()
            if k in self.req_sqlbase_list_search_time_types and v:      # 处理时间查询参数，str类型
                if not isinstance(v, str):
                    return Status(
                        213, 'failure', u'请求参数%s为字符串类型' % k or StatusMsgs.get(213), {}).json()
                if v:
                    try:
                        s2d(v)
                    except:
                        return Status(
                            213, 'failure', u'请求参数%s格式：yyyy-MM-dd HH:mm:ss' % k, {}).json()

            if k in self.req_sqlbase_list_search_like_types and v:      # like 查询参数
                v = '%' + str(v) + '%'
            elif k in self.req_sqlbase_list_search_int_types and v:      # int类型查询参数
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
        # 追加数据库类型，关联enum表
        new_params['enum_name'] = 'db-type'
        res, total = self.sqlbase_bo.get_all(new_params)
        """ all user k-v list"""
        user_res, _ = self.sysuser_bo.get_all({}, is_admin=True, is_del=True)
        user_list = list()
        for _d in user_res:
            if not _d: continue
            user_list.append({'key': _d.rtx_id, 'value': _d.fullname})
        """
        # 非分组型数据库类型枚举
        database_res = self.enum_bo.get_model_by_name(name='db-type')
        database_list = list()
        for _d in database_res:
            if not _d: continue
            database_list.append({'key': _d.key, 'value': _d.value})
        """
        database_list = self._group_database_types()
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101),
                {'list': [], 'total': 0, 'user': user_list, 'database': database_list}).json()
        # ////////////////// return data \\\\\\\\\\\\\\\\\\\\\
        """ sqlbase list """
        new_res = list()
        n = 1 + new_params.get('offset')
        for _d in res:
            if not _d: continue
            _res_dict = self._sqlbase_model_to_dict(_d, _type='list')
            if _res_dict:
                _res_dict['id'] = n
                # 权限账户
                _res_dict['edit'] = 'true' if req_rtx_id in auth_rtx_join([_res_dict.get('rtx_id')]) else 'false'
                new_res.append(_res_dict)
                n += 1
                
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
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_sqlbase_add_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
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

    def _group_database_types(self) -> list:
        """
        format database types by groups
            - 关系型数据库
            - 非关系型数据库
        """
        database_res = self.enum_bo.get_model_by_name(name='db-type')
        # return result
        _res = list()
        # 关系型数据库
        _rel_db_list = list()
        # 非关系型数据库
        _no_rel_db_list = list()
        # 其他数据库
        _other_db_list = list()
        for _d in database_res:
            if not _d: continue
            if not getattr(_d, 'description', ''): continue
            # 把非关系排在前面，否则都为关系型
            if str(_d.description).find('非关系型数据库') > -1:
                _rel_db_list.append({'key': _d.key, 'value': _d.value})
            elif str(_d.description).find('关系型数据库') > -1:
                _no_rel_db_list.append({'key': _d.key, 'value': _d.value})
            else:
                _other_db_list.append({'key': _d.key, 'value': _d.value})
        # 分组label排序
        if _no_rel_db_list:
            _res.append({'label': '非关系型数据库', 'options': _no_rel_db_list})
        if _rel_db_list:
            _res.append({'label': '关系型数据库', 'options': _rel_db_list})
        # 其他默认值
        # if not _other_db_list:
            # _other_db_list = [{'key': 'no', 'value': '暂无分类'}]
        if _other_db_list:
            _res.append({'label': '其他型', 'options': _other_db_list})
        return _res

    def sqlbase_add_init(self, params: dict) -> json:
        """
        sqlbase add data initialize enum list
        :return: json data
        """
        # ================== parameters check && format ==================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_add_init_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_add_init_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k or StatusMsgs.get(213), {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k or StatusMsgs.get(214), {}).json()
            new_params[k] = str(v)

        # <<<<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>>>>
        # enum: all users
        user_res, _ = self.sysuser_bo.get_all({}, is_admin=True, is_del=True)
        user_list = list()
        for _d in user_res:
            if not _d: continue
            user_list.append({'key': _d.rtx_id, 'value': _d.fullname})
        # enum: all database type
        """
        # 非分组型数据库类型枚举
        database_res = self.enum_bo.get_model_by_name(name='db-type')
        database_list = list()
        for _d in database_res:
            if not _d: continue
            database_list.append({'key': _d.key, 'value': _d.value})
        """
        database_list = self._group_database_types()
        _res = {
            'user': user_list,
            'database': database_list
        }
        return Status(
            100, 'success', StatusMsgs.get(100), _res).json()

    def sqlbase_delete(self, params: dict) -> json:
        """
        delete one sqlbase data by md5 from sqlbase table
        params is dict
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_delete_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_delete_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k or StatusMsgs.get(213), {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k or StatusMsgs.get(214), {}).json()
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
        # 权限账户
        if rtx_id not in auth_rtx_join([model.rtx_id]):
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
        delete many sqlbase data by md5 list from sqlbase table
        params is dict
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_deletes_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_deletes_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k or StatusMsgs.get(213), {}).json()
            if not v:   # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k or StatusMsgs.get(214), {}).json()
            if k == 'list':     # check type
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)
        # **************** 管理员获取ALL数据 *****************
        # 权限账号
        if new_params.get('rtx_id') in auth_rtx_join([]):
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
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_detail_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_detail_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k or StatusMsgs.get(213), {}).json()
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

        """ =============== return data =============== """
        # enum: all users
        user_res, _ = self.sysuser_bo.get_all({}, is_admin=True, is_del=True)
        user_list = list()
        for _d in user_res:
            if not _d: continue
            user_list.append({'key': _d.rtx_id, 'value': _d.fullname})
        # enum: all database type
        """
        # 非分组型数据库类型枚举
        database_res = self.enum_bo.get_model_by_name(name='db-type')
        database_list = list()
        for _d in database_res:
            if not _d: continue
            database_list.append({'key': _d.key, 'value': _d.value})
        """
        database_list = self._group_database_types()
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
        update sqlbase message information by data md5, contain:
            - title 标题
            - html/text 内容
            - author 作者
            - public—time 发布时间
            - recommend 推荐度
            - database 数据库
            - summary 简述
            - label 标签

        :return: json data
        """
        # ====================== parameters check and format ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_md5_necessary_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_sqlbase_update_attrs and v:      # 不合法参数
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k or StatusMsgs.get(213), {}).json()
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
        # 权限账户
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()

        # --------------------------------------- update model --------------------------------------
        for key, value in new_params.items():
            if not key: continue
            # 不更新属性
            if key in self.req_sqlbase_no_update_attrs: continue
            setattr(model, key, value)
        try:
            self.sqlbase_bo.merge_model(model)
            return Status(
                100, 'success', StatusMsgs.get(100), {'md5': model.md5_id}).json()
        except:
            return Status(
                450, 'failure', StatusMsgs.get(450), {'md5': model.md5_id}).json()

    def share_list(self, params: dict) -> json:
        """
        get share data list from db table share by parameters
        :return: many json data
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
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_share_list_attrs and v:  # is illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k or StatusMsgs.get(213), {}).json()

            if k in self.req_share_list_search_list_types:    # 处理列表参数
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s为列表类型' % k or StatusMsgs.get(213), {}).json()
            if k in self.req_share_list_search_time_types and v:      # 处理时间查询参数，str类型
                if not isinstance(v, str):
                    return Status(
                        213, 'failure', u'请求参数%s为字符串类型' % k or StatusMsgs.get(213), {}).json()
                if v:
                    try:
                        s2d(v)
                    except:
                        return Status(
                            213, 'failure', u'请求参数%s格式：yyyy-MM-dd HH:mm:ss' % k, {}).json()

            if k in self.req_share_list_search_like_types and v:      # like 查询参数
                v = '%' + str(v) + '%'
            elif k in self.req_share_list_search_int_types and v:      # int类型查询参数
                if not str(v).isdigit():
                    return Status(
                        213, 'failure', u'请求参数%s为数字类型' % k, {}).json()
                v = int(v)
            elif k == 'limit':
                v = int(v) if v else OFFICE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            # 参数写入new-params
            new_params[k] = v

        # **************** 全员获取ALL数据 *****************
        req_rtx_id = new_params.get('rtx_id')
        new_params.pop('rtx_id')
        '''
        # <get data>
        res, total = self.sqlbase_bo.get_all(new_params)
        """ return data list """
        new_res = list()
        n = 1 + new_params.get('offset')
        for _d in res:
            if not _d: continue
            _res_dict = self._sqlbase_model_to_dict(_d, _type='list')
            if _res_dict:
                _res_dict['id'] = n
                # 权限账户
                _res_dict['edit'] = 'true' if req_rtx_id in auth_rtx_join([_res_dict.get('rtx_id')]) else 'false'
                new_res.append(_res_dict)
                n += 1
        '''
        total = 11
        new_res = {
            '1': [
                {'id': 1, 'md5': 'A', 'name': 'Python 2.7.X 官方教程中文版', 'image': 'http://www.pythondoc.com/img/python27.png', 'url': 'http://www.pythondoc.com/flask-testing/index.html', 'summary': 'The Python Tutorial (Python 2.7.X) 的中文翻译版本。Python Tutorial 为初学 Python 必备官方教程，本教程适用于 Python 2.7.X 系列。'},
                {'id': 2, 'md5': 'B', 'name': 'Python 3.6.X 官方教程中文版', 'image': 'http://www.pythondoc.com/img/python3.png', 'url': 'http://www.pythondoc.com/pythontutorial3/index.html', 'summary': 'The Python Tutorial (Python 3.6.X) 的中文翻译版本。Python Tutorial 为初学 Python 必备官方教程，本教程适用于 Python 3.6.X。'},
                {'id': 3, 'md5': 'C', 'name': 'Flask官方教程【中文翻译】', 'image': 'http://www.pythondoc.com/img/flask.png', 'url': 'http://www.pythondoc.com/flask/index.html', 'summary': 'Flask 是一个轻量级的 Web 应用框架。其 WSGI 工具箱采用 Werkzeug ，模板引擎则使用 Jinja2。本教程适用于 Flask 0.10.1 以上版本。'},
                {'id': 4, 'md5': 'D', 'name': 'Flask Restful API中文教程', 'image': 'http://www.pythondoc.com/img/flask-restful.png', 'url': 'http://www.pythondoc.com/Flask-RESTful/index.html', 'summary': 'Flask-RESTful 为 Flask 添加了快速构建 REST APIs 的支持。'}
            ],
            '2': [
                {'id': 5, 'md5': 'E', 'name': 'Flask+SQLAlchemy+Postgresql异步方案', 'image': 'http://www.pythondoc.com/img/flaskasyn.png', 'url': 'http://www.pythonpub.com/article/1499', 'summary': 'Flask + SQLAlchemy + Postgresql 异步方案示例，为 Flask 开发提供数据库异步参考。'},
                {'id': 6, 'md5': 'F', 'name': 'Flask-SQLAlchmey中文教程', 'image': 'http://www.pythondoc.com/img/flaskalchemy.png', 'url': 'http://www.pythondoc.com/flask-sqlalchemy/index.html', 'summary': 'Flask-SQLAlchmey 为 Flask 提供了简单且有用的 SQLAlchmey 集成。'},
                {'id': 7, 'md5': 'G', 'name': 'Flask-Testing单元测试教程', 'image': 'http://www.pythondoc.com/img/flasktesting.png', 'url': 'http://www.pythondoc.com/flask-testing/index.html', 'summary': 'Flask-Testing 为 Flask 提供了单元测试的工具。'},
                {'id': 8, 'md5': 'H', 'name': 'Flask Restful API设计', 'image': 'http://www.pythondoc.com/img/flaskret.png', 'url': 'http://www.pythondoc.com/flask-restful/index.html', 'summary': 'Miguel 编写的使用 Python 以及 Flask 编写 RESTful API。'}
            ],
            '3': [
                {'id': 9, 'md5': 'I', 'name': 'Explore Flask中文教程', 'image': 'http://www.pythondoc.com/img/exploreflask.png', 'url': 'http://www.pythondoc.com/exploreflask/index.html', 'summary': '探索 Flask 是一本关于使用 Flask 开发 Web 应用程序的最佳实践和模式的书籍。这本书是 Flask 官方教程的一个有力的补充材料。适合进阶使用。'},
                {'id': 10, 'md5': 'J', 'name': 'Flask-Exceptional 中文翻译', 'image': 'http://www.pythondoc.com/img/flaskexc.png', 'url': 'http://www.pythondoc.com/flask-exceptional/index.html', 'summary': 'Flask-Exceptional 是一个为 Flask 添加 Exceptional 支持。'},
                {'id': 11, 'md5': 'K', 'name': 'Flask-Cache 中文翻译', 'image': 'http://www.pythondoc.com/img/flaskcache.png', 'url': 'http://www.pythondoc.com/flask-cache/index.html', 'summary': 'Flask-Cache 是一个用于 Flask 作为缓存的第三方扩展。'}
            ]
        }
        """ all user k-v list"""
        user_res, _ = self.sysuser_bo.get_all({}, is_admin=True, is_del=True)
        user_list = list()
        for _d in user_res:
            if not _d: continue
            user_list.append({'key': _d.rtx_id, 'value': _d.fullname})

        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total, 'user': user_list}
        ).json()

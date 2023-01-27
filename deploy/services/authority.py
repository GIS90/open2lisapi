# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    authority services

base_info:
    __author__ = "PyGo"
    __time__ = "2022/5/9 22:53"
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
# usage: /usr/bin/python authority.py
# ------------------------------------------------------------
import datetime
import json
from operator import itemgetter
from itertools import groupby

from deploy.utils.status_msg import StatusMsgs
from deploy.utils.status import Status
from deploy.bo.role import RoleBo
from deploy.bo.menu import MenuBo
from deploy.bo.sysuser import SysUserBo
from deploy.bo.enum import EnumBo

from deploy.config import AUTH_LIMIT, AUTH_NUM, \
    ADMIN, ADMIN_AUTH_LIST, MENU_ONE_LEVEL, MENU_ROOT_ID, \
    USER_DEFAULT_AVATAR, USER_DEFAULT_PASSWORD, USER_DEFAULT_INTROD
from deploy.utils.utils import d2s, get_now, md5, check_length


class AuthorityService(object):
    """
    authority service
    """

    DEFAULT_COMPONENT = 'layout'

    req_role_list_attrs = [
        'rtx_id',
        'limit',
        'offset'
    ]

    req_role_add_attrs = [
        'rtx_id',
        'engname',
        'chnname',
        'introduction'
    ]

    req_role_add_check_len_attrs = {
        'rtx_id': 25,
        'engname': 25,
        'chnname': 35
    }

    req_role_update_attrs = [
        'rtx_id',
        'md5',
        'engname',
        'chnname',
        'introduction'
    ]

    req_role_delete_attrs = [
        'rtx_id',
        'md5'
    ]

    req_role_deletes_attrs = [
        'rtx_id',
        'list'
    ]

    req_role_auth_attrs = [
        'rtx_id',
        'md5',
        'keys'
    ]

    role_list_attrs = [
        'id',
        'engname',
        'chnname',
        'md5_id',
        # 'authority', # 先不展示，因为是一个menu字符串
        'introduction',
        'create_time',
        'create_rtx',
        'delete_time',
        'delete_rtx',
        'is_del'
    ]

    req_user_list_attrs = [
        'rtx_id',
        'limit',
        'offset'
    ]

    req_user_kv_list_attrs = [
        'rtx_id'
    ]

    user_list_attrs = [
        'id',
        'rtx_id',
        'md5_id',
        'fullname',
        'password',
        'email',
        'phone',
        'avatar',
        'introduction',
        'department',
        'role',
        'create_time',
        'create_rtx',
        'delete_time',
        'delete_rtx',
        'is_del'
    ]

    req_user_add_attrs = [
        'add_rtx_id',
        'rtx_id',
        'name',
        'phone',
        'password',
        'email',
        'role',
        'introduction'
    ]

    req_user_status_attrs = [
        'rtx_id',
        'c_rtx_id',
        'status'
    ]

    req_user_deletes_attrs = [
        'rtx_id',
        'list'
    ]

    req_user_update_attrs = [
        'to_rtx_id',
        'rtx_id',
        'name',
        'phone',
        'email',
        'role',
        'introduction'
    ]

    menu_list_attrs = [
        'id',
        'name',
        'path',
        'title',
        'pid',
        'level',
        'md5_id',
        'order_id',
        'component',
        'hidden',
        'redirect',
        'icon',
        'cache',
        'affix',
        'breadcrumb',
        'create_time',
        'create_rtx',
        'is_del',
        'delete_time',
        'delete_rtx',
        'shortcut'
    ]

    req_menu_info_attrs = [
        'rtx_id',
        'md5'
    ]

    req_menu_update_attrs = [
        'rtx_id',
        'md5',
        'name',
        'title',
        'path',
        'icon',
        'pid',
        'level',
        'order_id',
        'component',
        'redirect',
        'hidden',
        'cache',
        'affix',
        'breadcrumb',
        'shortcut'
    ]

    req_menu_no_need_attrs = [
        'redirect',
        'order_id'
    ]

    req_menu_int_update_attrs = [
        'pid',
        'level'
    ]

    req_menu_bool_update_attrs = [
        'hidden',
        'cache',
        'affix',
        'breadcrumb',
        'shortcut'
    ]

    req_menu_ckeck_len_attrs = {
        'rtx_id': 25,
        'name': 25,
        'title': 25,
        'path': 35,
        'icon': 25,
        'component': 25,
        'redirect': 35
    }

    req_menu_add_attrs = [
        'rtx_id',
        'name',
        'title',
        'path',
        'icon',
        'pid',
        'level',
        'component',
        'redirect',
        'hidden',
        'cache',
        'affix',
        'breadcrumb',
        'shortcut',
        'order_id'
    ]

    req_menu_status_attrs = [
        'rtx_id',
        'md5',
        'status'
    ]

    def __init__(self):
        """
        authority service class initialize
        """
        super(AuthorityService, self).__init__()
        self.role_bo = RoleBo()
        self.menu_bo = MenuBo()
        self.sysuser_bo = SysUserBo()
        self.enum_bo = EnumBo()

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

    def _role_model_to_dict(self, model, is_detail=False):
        """
        role model to dict data
        return json data

        is_detail: detail information, 是否是缩略数据
        """
        if not model:
            return {}

        res = dict()
        for attr in self.role_list_attrs:
            if not attr:continue
            if attr == 'engname':
                res[attr] = getattr(model, 'engname', '')
            elif attr == 'chnname':
                res[attr] = getattr(model, 'chnname', '')
            elif attr == 'md5_id':
                res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'authority':
                res[attr] = getattr(model, 'authority', '')
            elif attr == 'introduction':
                introduction = getattr(model, 'introduction', '')
                if not is_detail:
                    res[attr] = introduction \
                        if introduction and len(introduction) < AUTH_NUM \
                        else '%s...查看详情' % str(introduction)[:AUTH_NUM-1]
                else:
                    res[attr] = introduction
            elif attr == 'create_time':
                res[attr] = self._transfer_time(model.create_time)
            elif attr == 'create_rtx':
                res[attr] = getattr(model, 'create_rtx', '')
            elif attr == 'delete_time':
                res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'delete_rtx':
                res[attr] = getattr(model, 'delete_rtx', '')
            elif attr == 'is_del':
                res[attr] = model.is_del or False
        else:
            return res

    def _user_model_to_dict(self, model, is_pass=False, is_detail=False):
        """
        role model to dict data
        return json data

        is_pass: is or not need password
        is_detail: is or not need detail, 主要用于是否超出字符限制
        """
        if not model:
            return {}

        _res = dict()
        for attr in self.user_list_attrs:
            if not attr: continue
            if attr == 'id':
                _res[attr] = getattr(model, 'id', '')
            elif attr == 'rtx_id':
                _res[attr] = getattr(model, 'rtx_id', '')
            elif attr == 'md5_id':
                _res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'fullname':
                _res['name'] = getattr(model, 'fullname', '')
            elif attr == 'password' and is_pass:
                _res[attr] = getattr(model, 'password', '')
            elif attr == 'email':
                _res[attr] = getattr(model, 'email', '')
            elif attr == 'phone':
                _res[attr] = getattr(model, 'phone', '')
            elif attr == 'avatar':
                _res[attr] = getattr(model, 'avatar', USER_DEFAULT_AVATAR)
            elif attr == 'introduction':
                introduction = getattr(model, 'introduction', '')
                if not is_detail:
                    _res[attr] = '%s...查看详情' % str(introduction)[0: AUTH_NUM-1] \
                        if introduction and len(introduction) > AUTH_NUM \
                        else introduction
                else:
                    _res[attr] = introduction
            elif attr == 'department':
                _res[attr] = getattr(model, 'department', '')
            elif attr == 'role':  # 多角色，存储role的engname，也就是role的rtx_id
                _res[attr] = str(model.role).split(';') if model.role else []
            elif attr == 'create_time':
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'create_rtx':
                _res[attr] = getattr(model, 'create_rtx', '')
            elif attr == 'is_del':
                _res[attr] = model.is_del or False
            elif attr == 'delete_time':
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'delete_rtx':
                _res[attr] = getattr(model, 'delete_rtx', '')
        else:
            return _res

    def _menu_model_to_dict(self, model, info=False):
        """
        menu model to dict data
        return json data
        :params info:
            - true：详情/编辑
            - false：table数据显示
        attrs:
            'id', 'name', 'path', 'title', 'pid', 'level', 'md5_id',
            'component', 'hidden', 'redirect', 'icon', 'cache', 'affix', 'breadcrumb',
            'create_time','create_rtx', 'is_del','delete_time','delete_rtx'
        """
        if not model:
            return {}

        _res = dict()
        for attr in self.menu_list_attrs:
            if not attr: continue
            if attr == 'id':
                _res[attr] = model.id
            elif attr == 'name':
                _res[attr] = model.name
            elif attr == 'path':
                _res[attr] = model.path
            elif attr == 'title':
                _res[attr] = model.title
            elif attr == 'pid':
                _res[attr] = model.pid
            elif attr == 'level':
                _res[attr] = str(model.level)
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'order_id':
                _res[attr] = model.order_id
            elif attr == 'component':
                _res[attr] = model.component
            elif attr == 'hidden':
                if info:
                    _res[attr] = '1' if model.hidden else '0'
                else:
                    _res[attr] = '是' if model.hidden else '否'
            elif attr == 'redirect':
                _res[attr] = model.redirect
            elif attr == 'icon':
                _res[attr] = model.icon
            elif attr == 'cache':
                if info:
                    _res[attr] = '1' if model.cache else '0'
                else:
                    _res[attr] = '是' if model.cache else '否'
            elif attr == 'affix':
                if info:
                    _res[attr] = '1' if model.affix else '0'
                else:
                    _res[attr] = '是' if model.affix else '否'
            elif attr == 'breadcrumb':
                if info:
                    _res[attr] = '1' if model.breadcrumb else '0'
                else:
                    _res[attr] = '是' if model.breadcrumb else '否'
            elif attr == 'create_time':
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'create_rtx':
                _res[attr] = model.create_rtx or ''
            elif attr == 'is_del':
                _res[attr] = True if model.is_del else False
            elif attr == 'delete_time':
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'delete_rtx':
                _res[attr] = model.delete_rtx or ""
            elif attr == 'shortcut':
                if info:
                    _res[attr] = '1' if model.is_shortcut else '0'
                else:
                    _res[attr] = '是' if model.is_shortcut else '否'
        else:
            return _res

    def role_list(self, params: dict) -> dict:
        """
        get role list, many parameters
        return json data

        default get role is no delete
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        # ------------------ parameters check -------------------
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_role_list_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v and k != 'offset':
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}
                ).json()
            if k == 'limit':
                v = int(v) if v else AUTH_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            else:
                v = str(v)
            new_params[k] = v

        # ///////////////// get data ///////////////////
        res, total = self.role_bo.get_all(new_params)       # 全部数据
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}
            ).json()
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            # if getattr(_d, 'engname') == ADMIN: continue     # 不显示管理员角色
            _res_dict = self._role_model_to_dict(_d)
            if _res_dict:       # 添加额外自定义ID序列
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def role_detail(self, params: dict) -> dict:
        """
        get role detail information
        by rtx id
        :return: json data
        """
        # =================== check parameters ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        role_md5 = params.get('md5')
        if not role_md5:
            return Status(
                212, 'failure', "缺少md5参数", {}).json()

        model = self.role_bo.get_model_by_md5(role_md5)
        # not exist
        if not model:
            return Status(
                302, 'failure', '角色不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                302, 'failure', '角色已删除' or StatusMsgs.get(302), {}).json()
        # check rtx-id and md5-id
        if not model.engname or not model.md5_id:
            return Status(
                313, 'failure', '角色信息不完整' or StatusMsgs.get(313), {}).json()
        # return
        return Status(
            100, 'success', StatusMsgs.get(100), self._role_model_to_dict(model, is_detail=True)
        ).json()

    def role_add(self, params: dict) -> dict:
        """
        add new role, information contain: english name, chinese name, introduction
        :return: json data

        new role model data
        """
        # >>>>>>>>> no parameters
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_role_add_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # parameters check length
        for _key, _value in self.req_role_add_check_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # ******************** check engname is or not repeat **********************
        model = self.role_bo.get_model_by_engname(new_params.get('engname'))
        if model:
            return Status(
                213, 'failure', '角色RTX已存在，请重新输入', {}).json()
        md5_id = md5(new_params.get('engname'))
        model_md5_id = self.role_bo.get_model_by_md5(md5=md5_id)
        if model_md5_id:
            return Status(
                213, 'failure', '角色MD5已存在，请重新输入RTX', {}).json()
        # ///////////////// add new model 、、、、、、、、、、
        try:
            new_model = self.role_bo.new_mode()
            new_model.engname = new_params.get('engname')
            new_model.chnname = new_params.get('chnname')
            new_model.md5_id = md5_id
            new_model.authority = ''
            new_model.introduction = new_params.get('introduction')
            new_model.create_time = get_now()
            new_model.create_rtx = new_params.get('rtx_id')
            new_model.is_del = False
            self.role_bo.add_model(new_model)
        except:
            return Status(
                320, 'failure', StatusMsgs.get(320), {'md5': md5_id}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': md5_id}
        ).json()

    def role_update(self, params: dict) -> dict:
        """
        update role, information contain:
            - chnname
            - introduction
        by role md5
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        # parameters check, engname is not allow update
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_role_update_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # parameters check length
        for _key, _value in self.req_role_add_check_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        if new_params.get('engname') == ADMIN:  # ***** 管理员角色不允许更新 *****
            return Status(
                213, 'failure', u'AMDIN角色为系统默认角色，不允许操作', {}).json()
        """ 其他特殊检查 """
        # check engname is or not repeat
        model = self.role_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在', {}).json()
        # data is delete
        if model and model.is_del:
            return Status(
                304, 'failure', '数据已删除，不允许更新', {}).json()
        # ADMIN用户不允许更新
        if model and model.engname == ADMIN:
            return Status(
                304, 'failure', '管理员角色不允许更新', {}).json()
        # role engname is not allow to update
        if str(model.engname).strip() != str(new_params.get('engname')).strip():
            return Status(
                304, 'failure', '角色RTX不允许更新', {}).json()
        try:
            model.chnname = new_params.get('chnname')
            model.introduction = new_params.get('introduction')
            self.role_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {'md5': new_params.get('md5')}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def role_batch_delete(self, params: dict) -> dict:
        """
        batch delete many role data, from role table
        post request and json parameters
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # request parameters check
            if k not in self.req_role_deletes_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # request value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            # list check
            if k == 'list':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)
        # ------------------- 检查批量删除的对象 -----------------------
        all_data = self.role_bo.get_models_by_md5list(new_params.get('list'))
        # not exist
        if not all_data:
            return Status(
                302, 'failure', u'请求删除数据不存在', {}).json()
        # 管理员角色不允许删除
        for _d in all_data:
            if not _d: continue
            if _d.engname == ADMIN:
                return Status(
                    302, 'failure', u'管理员角色不允许操作，请重新选择', {}).json()
        # **************** 管理员获取ALL数据 *****************
        ADMIN_AUTH_LIST.extend([ADMIN])     # 特权账号
        if new_params.get('rtx_id') in ADMIN_AUTH_LIST:
            new_params.pop('rtx_id')
        # ------------------- batch delete data -----------------------
        try:
            res = self.role_bo.batch_delete_by_md5(params=new_params)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()

        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list')) - res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list')) - res)}).json()

    def role_delete(self, params: dict) -> dict:
        """
        one delete many role data
        from role table
        post request and json parameters
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # 不合法的参数检查
            if k not in self.req_role_delete_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<< data model by md5 >>>>>>>>>>>>>
        model = self.role_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}).json()
        # ADMIN用户不允许删除
        if model and model.engname == ADMIN:
            return Status(
                304, 'failure', '管理员角色不允许删除', {}).json()
        # authority
        rtx_id = new_params.get('rtx_id')
        ADMIN_AUTH_LIST.extend([ADMIN, model.create_rtx])
        if rtx_id not in ADMIN_AUTH_LIST:
            return Status(
                311, 'failure', StatusMsgs.get(311), {}).json()
        # /////////////// 软删除数据
        try:
            model.is_del = True
            model.delete_rtx = rtx_id
            model.delete_time = get_now()
            self.role_bo.merge_model(model)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()
        
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def role_auth_tree(self, params: dict) -> dict:
        """
        get the role authority list
        :return: json data
        authority is tree
        """
        # ------------------- check parameters --------------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        if not params.get('md5'):
            return Status(
                214, 'failure', '缺少md5请求参数', {}).json()
        # ==================== check data ======================
        role_model = self.role_bo.get_model_by_md5(md5=params.get('md5'))
        # not exist
        if not role_model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # data is deleted
        if role_model and role_model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}).json()
        # ADMIN用户不允许设置
        if role_model and role_model.engname == ADMIN:
            return Status(
                304, 'failure', '管理员角色不允许设置', {}).json()
        # <<<<<<<<<<<<<<<<<< authority >>>>>>>>>>>>>>>>>>>>>>
        auths = str(role_model.authority).split(';') \
            if role_model.authority else []
        auth_list = [int(x) for x in auths if x]
        all_menus = self.menu_bo.get_all(root=False)
        # not menu data
        if not all_menus:
            return Status(
                101, 'failure', StatusMsgs.get(101), {}).json()

        """ 权限树 """
        _res = list()
        template_list = list()
        one_menus = dict()
        one_menu_keys = list()  # 默认展开一级菜单，后续改成展开权限菜单
        for menu in all_menus:
            if not menu or menu.is_del \
                    or not menu.id or not menu.title or not menu.level:
                continue
            _d = {'id': int(menu.id), 'pid': int(menu.pid), 'label': str(menu.title), 'disabled': False}
            if int(menu.level) == MENU_ONE_LEVEL:
                one_menus[menu.id] = _d
            else:
                template_list.append(_d)
            if int(menu.level) == MENU_ONE_LEVEL:
                one_menu_keys.append(int(menu.id))
        template_list.sort(key=itemgetter('pid'))
        for key, group in groupby(template_list, key=itemgetter('pid')):
            if key in one_menus.keys():
                _d = one_menus.get(key)
                _d['children'] = list(group)
                _res.append(_d)

        del template_list   # 处理临时变量
        """
        menus: 菜单
        auths: 角色的权限列表
        expand: 默认展开的一级菜单列表
        """
        return Status(
            100, 'success', StatusMsgs.get(100),
            {"menus": _res, "auths": auth_list, "expand": auth_list}
        ).json()

    def role_save_tree(self, params: dict) -> dict:
        """
        save role authority from db table role
        authority is list type, data is keys
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_role_auth_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            if k == 'keys':     # 菜单ID，也就是权限列表，List类型
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                new_v = [str(i) for i in v]
                # new_v = list(set(new_v))      # 去重
                v = ';'.join(new_v)
            new_params[k] = str(v)
        """ model """
        model = self.role_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}).json()
        # save authority
        try:
            model.authority = new_params.get('keys')
            self.role_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {'md5': new_params.get('md5')}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def role_select_list(self):
        """
        get role list select, no parameters
        data type: [{key, value}]
        :return: json data
        """
        res = self.role_bo.get_select_all()
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}
            ).json()
        new_res = list()
        for _d in res:
            if not _d or not _d.engname or not _d.chnname: continue
            new_res.append({'key': _d.engname, 'value': _d.chnname})
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': len(new_res)}
        ).json()

    def user_list(self, params: dict) -> dict:
        """
        get user list, many parameters: limit, offset
        return json data

        default get user is no delete
        """
        # ---------------------- parameters check ----------------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_user_list_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v and k != 'offset':
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            if k == 'limit':
                v = int(v) if v else AUTH_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            else:
                v = str(v)
            new_params[k] = v
        # /////////// return data
        res, total = self.sysuser_bo.get_all(new_params, is_admin=False)    # 全员数据
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        new_res = list()
        for _d in res:
            if not _d: continue
            # if getattr(_d, 'rtx_id') == ADMIN: continue     # 不显示管理员
            _res_dict = self._user_model_to_dict(_d)
            if _res_dict:
                new_res.append(_res_dict)
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def user_add(self, params: dict) -> dict:
        """
        add new user, information contain: rtx_id, name, phone,
        email, password, role, introduction
        add_rtx_id: 添加用户的账号rtx
        :return: json data

        new data:
        头像采用随机头像
        密码有个默认密码，在config中配置
        """
        # ================= check parameters: value, length ===================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        """ make new parameters """
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_user_add_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in ['password', 'email', 'introduction']:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            # check: length
            if k == 'rtx_id' and not check_length(v, 25):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'name' and not check_length(v, 30):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'phone' and len(v) != 11:
                return Status(
                    213, 'failure', u'正确电话为11位' % k, {}).json()
            elif k == 'email' and not check_length(v, 35):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'introduction' and not check_length(v, 255):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            # check: role
            if k == 'role':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                # TODO 可以加上role验证
                new_params[k] = ';'.join(v)
            elif k == 'rtx_id':
                new_params[k] = str(v).strip()    # rtx_id 去空格
            else:
                new_params[k] = str(v)

        # check rtx_id is or not exist
        if self.sysuser_bo.get_user_by_rtx_id(new_params.get('rtx_id')):
            return Status(
                213, 'failure', '用户RTX-ID已存在，请重新输入', {}).json()
        # check phone is or not exist
        if new_params.get('phone') and \
                self.sysuser_bo.get_user_by_phone(new_params.get('phone')):
            return Status(
                213, 'failure', '用户电话已存在，请重新输入', {}).json()
        # check email is or not exist
        if new_params.get('email') and \
                self.sysuser_bo.get_user_by_email(new_params.get('email')):
            return Status(
                213, 'failure', '用户邮箱已存在，请重新输入', {}).json()
        ''' add new model '''
        md5_id = md5(new_params.get('rtx_id'))
        try:
            new_model = self.sysuser_bo.new_mode()
            new_model.rtx_id = new_params.get('rtx_id')
            new_model.fullname = new_params.get('name')
            new_model.md5_id = md5_id
            new_model.password = new_params.get('password') or USER_DEFAULT_PASSWORD    # 默认密码
            new_model.phone = new_params.get('phone') or ""
            new_model.email = new_params.get('email') or ""
            new_model.avatar = USER_DEFAULT_AVATAR  # 新增用户默认头像
            new_model.department = ""
            new_model.role = new_params.get('role') or ""
            new_model.introduction = new_params.get('introduction') or USER_DEFAULT_INTROD  # 默认米哦啊叔
            new_model.create_time = get_now()
            new_model.create_rtx = new_params.get('add_rtx_id')
            new_model.is_del = False
            new_model.delete_time = ''
            self.sysuser_bo.add_model(new_model)
        except:
            return Status(
                320, 'failure', StatusMsgs.get(320), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': md5_id}
        ).json()

    def user_batch_delete(self, params: dict) -> dict:
        """
        batch delete many user data, from sysuser table
        post request and json parameters
        :return: json data
        """
        # parameters check
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_user_deletes_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            if k == 'list':     # type check
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)
        # ------------------------ model ------------------------
        all_data = self.sysuser_bo.get_models_by_md5_list(new_params.get('list'))
        # not exist
        if not all_data:
            return Status(
                302, 'failure', u'注销用户不存在', {}).json()
        # 管理不允许注销
        for _d in all_data:
            if not _d: continue
            if _d.rtx_id == ADMIN:
                return Status(
                    302, 'failure', u'管理员用户不允许注销，请重新选择', {}).json()
        # batch注销
        try:
            res = self.sysuser_bo.batch_delete_by_md5_list(params=new_params)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()
        return Status(100, 'success', '用户注销成功' or StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(100, 'failure', "成功：[%s]，失败：[%s]" % (res, (len(new_params.get('list')) - res)),
                        {'success': res, 'failure': (len(new_params.get('list')) - res)}).json()

    def user_status(self, params: dict) -> dict:
        """
        one change user data status
        from user table
        post request and json parameters
        :return: json data

        状态改变：
        true：注销
        false：启用
        """
        # not parameters
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_user_status_attrs:
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
        # <<<<<<<<<<<<< get data model >>>>>>>>>>>>>>>
        model = self.sysuser_bo.get_user_by_rtx_id(rtx_id=new_params.get('c_rtx_id'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '用户不存在' or StatusMsgs.get(302), {}).json()
        # 管理员不允许操作
        if model.rtx_id == ADMIN:
            return Status(
                300, 'failure', '管理员用户不允许操作' or StatusMsgs.get(300), {}).json()
        # ----------- change status -----------
        try:
            model.is_del = new_params.get('status')
            if new_params.get('status'):
                model.delete_rtx = new_params.get('rtx_id')
                model.delete_time = get_now()
            self.role_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {}).json()
        message = '用户注销成功' if new_params.get('status') else '用户启用成功'
        return Status(
            100, 'success', message or StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def user_detail(self, params: dict) -> dict:
        """
        get user detail information
        by rtx id
        :return: json data

        data:
            - user base info
            - role list (select)
        """
        # =================== check parameters ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # check rtx_id is or not exist
        rtx_id = params.get('rtx_id')
        if not rtx_id:
            return Status(
                302, 'failure', '用户不存在' or StatusMsgs.get(302), {}).json()
        model = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        # not exist
        if not model:
            return Status(
                302, 'failure', '用户不存在' or StatusMsgs.get(302), {}).json()
        # deleted: 先查看启用、注销2种状态的数据
        # if model and model.is_del:
        #     return Status(
        #         302, 'failure', '用户已注销' or StatusMsgs.get(302), {}).json()

        # user base info
        model_res = self._user_model_to_dict(model, is_pass=False, is_detail=True)
        # role select list
        roles_res = json.loads(self.role_select_list()) or {}
        model_res['roles'] = roles_res.get('data').get('list') or [] \
            if roles_res.get('status_id') == 100 else []
        return Status(
            100, 'success', StatusMsgs.get(100), model_res
        ).json()

    def user_update(self, params):
        """
        update user, information contain:
            - name
            - phone
            - email
            - role
            - introduction
        by user rtx id
        :return: json data
        """
        """   ========== check parameters ============"""
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_user_update_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in ['email', 'introduction']:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            # check: length
            if k == 'name' and not check_length(v, 30):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'phone' and len(v) != 11:
                return Status(
                    213, 'failure', u'正确电话为11位' % k, {}).json()
            elif k == 'email' and not check_length(v, 35):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'introduction' and not check_length(v, 255):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            # check: role
            if k == 'role':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                # TODO 可以加上role验证
                new_params[k] = ';'.join(v)
            else:
                new_params[k] = str(v)

        model = self.sysuser_bo.get_user_by_rtx_id(new_params.get('to_rtx_id'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在', {}).json()
        # data is delete: 注销 && 启用状态均可以更新
        # if model and model.is_del:
        #     return Status(
        #         304, 'failure', '数据已删除，不允许更新', {}).json()
        # 管理员不允许操作
        if model.rtx_id == ADMIN:
            return Status(
                300, 'failure', '管理员用户不允许操作' or StatusMsgs.get(300), {}).json()

        # <<<<<<<<<<<<<<<< update user model >>>>>>>>>>>>>>>>>>
        try:
            model.fullname = new_params.get('name')
            model.phone = new_params.get('phone')
            model.email = new_params.get('email')
            model.role = new_params.get('role')
            model.introduction = new_params.get('introduction') or USER_DEFAULT_INTROD
            self.sysuser_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {}
        ).json()

    def user_reset_pw(self, params: dict) -> dict:
        """ 重置用户默认密码
        reset user password
        default is abc1234
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        rtx_id = params.get('rtx_id')
        # check rtx_id is or not exist
        model = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        # not exist
        if not model:
            return Status(
                302, 'failure', '用户不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                302, 'failure', '用户已注销' or StatusMsgs.get(302), {}).json()
        try:
            # reset password
            # 方式一
            setattr(model, 'password', USER_DEFAULT_PASSWORD)
            self.sysuser_bo.merge_model_no_trans(model)
            # 方式二
            # model.password = USER_DEFAULT_PASSWORD
            # self.sysuser_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {}).json()

    def menu_list(self, params: dict) -> dict:
        """
        get menu list from db table menu
        return json data

        思路：1.获取全部数据，包含禁用的菜单
        2.进行过滤分组，一级菜单 && 二级临时菜单
        3.二级临时菜单按pid父节点ID进行group分组
        4.二级临时菜单加入到一级菜单的children
        5.return dara

        default get menu is all
        data structure:
        [{
          id: 1,
          date: '2016-05-02',
          name: 'XXXX'
        }, {
          id: 2,
          date: '2016-05-01',
          name: 'YYYY'
          children: [{
              id: 21,
              date: '2016-05-01',
              name: 'YYYY-01'
            }]
        }]

        难点：数据结构
        """
        # ///////////////// check parameters \\\\\\\\\\\\\\\\\
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        rtx_id = params.get('rtx_id')
        if not rtx_id:
            return Status(
                214, 'failure', u'缺少rtx_id请求参数', {}).json()
        # ------------------ get all menus ------------------
        all_menus = self.menu_bo.get_all_no(root=True)   # 全部数据，包含禁用菜单 根节点0
        if not all_menus:
            return Status(
                101, 'failure', StatusMsgs.get(101), {}).json()
        # 格式化菜单
        _res = list()
        template_list = list()  # 二级临时菜单
        one_menus = dict()  # 一级菜单
        one_menus_keys = list()  # 菜单一级节点keys，List类型，存储格式：[{'id': menu.id}, {'id': menu.id}...]
        root_menu = dict()  # 菜单根节点，只有一个
        # 所有菜单，遍历之后加入一级菜单列表、临时菜单列表（二级）
        for menu in all_menus:
            if not menu: continue
            _d = self._menu_model_to_dict(menu, info=False)
            if not _d: continue
            if int(menu.level) == MENU_ONE_LEVEL:
                one_menus[menu.id] = _d
                one_menus_keys.append({'id': menu.id})
            else:
                template_list.append(_d)
            if int(menu.id) == MENU_ROOT_ID:
                root_menu['id'] = str(menu.id)
                root_menu['name'] = menu.name
                root_menu['title'] = menu.title

        template_list.sort(key=itemgetter('pid'))
        # 二级菜单分组，加入新的数据列表
        for key, group in groupby(template_list, key=itemgetter('pid')):
            if key in one_menus.keys():
                _d = one_menus.get(key)
                _new_child = list()
                for g in group:
                    if not g: continue
                    if _d.get('path'):
                        g['path'] = '%s/%s' % (_d.get('path'), g.get('path'))
                    # 二级菜单加入父节点信息（一级菜单）
                    g['pname'] = _d.get('name')
                    g['ptitle'] = _d.get('title')
                    _new_child.append(g)
                # 二级菜单排序
                _new_sort_child = sorted(_new_child, key=itemgetter('order_id'), reverse=False)
                _d['children'] = _new_sort_child
                # 一级菜单加入根节点信息
                _d['pid'] = root_menu.get('id') or "0"
                _d['pname'] = root_menu.get('name') or "Home"
                _d['ptitle'] = root_menu.get('title') or "首页"
                _res.append(_d)
        # 删除临时列表
        del template_list
        # 一级菜单菜单排序
        sort_res = sorted(_res, key=itemgetter('order_id'), reverse=False)

        return Status(
            100, 'success', StatusMsgs.get(100), {'list': sort_res, 'keys': one_menus_keys}
        ).json()

    def menu_detail(self, params: dict) -> dict:
        """
        get menu detail information from db table menu, menu is dict object
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        # ------------ parameters check ---------------
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_menu_info_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<< model >>>>>>>>>>>>>
        model = self.menu_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '菜单不存在' or StatusMsgs.get(302), {}).json()
        model_res = self._menu_model_to_dict(model, info=True)
        # 获取根节点 && 一级菜单
        root_one_menu_models = self.menu_bo.get_root_one_menus()
        root_menu = list()  # 菜单根节点，只有一个
        one_menus = list()  # 一级菜单，多个List类型
        for menu in root_one_menu_models:
            if not menu: continue
            root_menu.append({'label': menu.title, 'value': str(menu.id)}) \
                if int(menu.id) == MENU_ROOT_ID \
                else one_menus.append({'label': menu.title, 'value': str(menu.id)})
        menu_options = [
            {'label': "根节点", 'options': root_menu},
            {'label': "一级菜单", 'options': one_menus}
        ]

        # enum info
        names = ['menu-level', 'bool-type']
        enums_models = self.enum_bo.get_model_by_names(names)
        template_list = list()
        for e in enums_models:
            template_list.append({'name': str(e.name), 'label': str(e.value), 'value': str(e.key)})
        enums_models_dict = dict()
        template_list.sort(key=itemgetter('name'))
        for key, group in groupby(template_list, key=itemgetter('name')):
            enums_models_dict[key] = list(group)
        # pid 字符串
        model_res['pid'] = str(model_res.get('pid'))
        data = {
            'menu': model_res,
            'level_enmus': enums_models_dict.get('menu-level'),
            'bool_enmus': enums_models_dict.get('bool-type'),
            'menu_options': menu_options
        }
        return Status(
            100, 'success', StatusMsgs.get(100), data).json()

    def menu_add(self, params: dict) -> dict:
        """
        add new menu information to db table menu
        menu is dict object
        :return: json data
        """
        # ===== check parameters && format parameters ======
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_menu_add_attrs:    # illegal
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v and k not in self.req_menu_no_need_attrs:  # is not null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()

            if k in self.req_menu_bool_update_attrs:
                v = True if str(v) == '1' else False
            elif k in self.req_menu_int_update_attrs:
                v = int(v)
            else:
                v = str(v)
            new_params[k] = v

        # parameters length check
        for _key, _value in self.req_menu_ckeck_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()
        # 顺序ID特殊判断处理
        order_id = str(new_params.get('order_id'))
        if not order_id:
            new_params['order_id'] = 1

        # check name is or not exist, name is unique
        model = self.menu_bo.get_model_by_name(new_params.get('name'))
        # model is exist
        if model:
            return Status(
                302, 'failure', '菜单RTX名称已存在' or StatusMsgs.get(302), {}).json()
        """ add new model """
        try:
            # create new model
            new_model = self.menu_bo.new_mode()
            # 默认值
            new_params['md5_id'] = md5(new_params.get('name'))
            new_params['create_time'] = get_now()
            new_params['is_del'] = False
            # shortcut 特殊处理
            new_params['is_shortcut'] = new_params.get('shortcut')
            new_params.pop('shortcut')
            for key, value in new_params.items():
                if not key: continue
                if key == 'rtx_id':
                    setattr(new_model, 'create_rtx', value)
                else:
                    setattr(new_model, key, value)
            else:
                self.menu_bo.add_model(new_model)
        except:
            return Status(
                320, 'failure', StatusMsgs.get(320), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {}).json()

    def menu_add_init(self) -> dict:
        """
        initialize add menu information from db table menu, menu is dict object
        no parameters
        :return: json data
        data is enums: bool, one level menus
        """
        # 获取根节点 && 一级菜单
        root_one_menu_models = self.menu_bo.get_root_one_menus()
        root_menu = list()  # 菜单根节点，只有一个
        one_menus = list()  # 一级菜单，多个List类型
        for menu in root_one_menu_models:
            if not menu: continue
            root_menu.append({'label': menu.title, 'value': str(menu.id)}) \
                if int(menu.id) == MENU_ROOT_ID \
                else one_menus.append({'label': menu.title, 'value': str(menu.id)})
        menu_options = [
            {'label': "根节点", 'options': root_menu},
            {'label': "一级菜单", 'options': one_menus}
        ]

        # enum info
        names = ['menu-level', 'bool-type']
        enums_models = self.enum_bo.get_model_by_names(names)
        template_list = list()
        for e in enums_models:
            template_list.append({'name': str(e.name), 'label': str(e.value), 'value': str(e.key)})
        enums_models_dict = dict()
        template_list.sort(key=itemgetter('name'))
        for key, group in groupby(template_list, key=itemgetter('name')):
            enums_models_dict[key] = list(group)
        data = {
            'level_enmus': enums_models_dict.get('menu-level'),
            'bool_enmus': enums_models_dict.get('bool-type'),
            'menu_options': menu_options
        }
        return Status(
            100, 'success', StatusMsgs.get(100), data).json()

    def menu_update(self, params: dict) -> dict:
        """
        update menu detail information from db table menu, menu is dict object
        :return: json data
        """
        # parameters check && format parameters
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_menu_update_attrs:  # illegal
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v and k not in self.req_menu_no_need_attrs:  # is not null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()

            if k in self.req_menu_bool_update_attrs:
                v = True if str(v) == '1' else False
            elif k in self.req_menu_int_update_attrs:
                v = int(v)
            else:
                v = str(v)
            new_params[k] = v

        # parameters length check
        for _key, _value in self.req_menu_ckeck_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()
        # 顺序ID特殊判断处理
        order_id = str(new_params.get('order_id'))
        if not order_id:
            new_params['order_id'] = 1

        # <<<<<<<<<<<<< ======== model by md5 ======== >>>>>>>>>>>>>>
        model = self.menu_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '菜单不存在' or StatusMsgs.get(302), {}).json()
        # update model
        # 只有新旧值不一致更新
        try:
            if model.name != new_params.get('name'):
                model.name = new_params.get('name')
            if model.path != new_params.get('path'):
                model.path = new_params.get('path')
            if model.title != new_params.get('title'):
                model.title = new_params.get('title')
            if model.pid != new_params.get('pid'):
                model.pid = new_params.get('pid')
            if model.level != new_params.get('level'):
                model.level = new_params.get('level')
            if model.component != new_params.get('component'):
                model.component = new_params.get('component') or self.DEFAULT_COMPONENT
            if model.redirect != new_params.get('redirect'):
                model.redirect = new_params.get('redirect')
            if model.icon != new_params.get('icon'):
                model.icon = new_params.get('icon')
            if model.hidden != new_params.get('hidden'):
                model.hidden = new_params.get('hidden')
            if model.cache != new_params.get('cache'):
                model.cache = new_params.get('cache')
            if model.affix != new_params.get('affix'):
                model.affix = new_params.get('affix')
            if model.breadcrumb != new_params.get('breadcrumb'):
                model.breadcrumb = new_params.get('breadcrumb')
            if model.order_id != new_params.get('order_id'):
                model.order_id = new_params.get('order_id')
            if model.is_shortcut != new_params.get('shortcut'):
                model.is_shortcut = new_params.get('shortcut')
            self.menu_bo.merge_model(model)
        except:
            return Status(
                322, 'success', StatusMsgs.get(322), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {}).json()

    def menu_status(self, params: dict) -> dict:
        """
        change menu data status, from menu table
        post request and json parameters
        :return: json data

        状态改变：
        true：注销
        false：启用
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_menu_status_attrs:     # 不合法请求参数
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

        model = self.menu_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '菜单不存在' or StatusMsgs.get(302), {}).json()
        # change status
        try:
            model.is_del = new_params.get('status')
            if new_params.get('status'):
                model.delete_rtx = new_params.get('rtx_id')
                model.delete_time = get_now()
            self.menu_bo.merge_model(model)
        except:
            return Status(
                322, 'success', StatusMsgs.get(322), {'md5': new_params.get('md5')}).json()
        message = '菜单禁用成功' if new_params.get('status') else '菜单启用成功'
        return Status(
            100, 'success', message or StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def user_kv_list(self, params: dict) -> dict:
        """
        get user list
        return json data

        default get user is no delete

        key-value格式：
            {'key': _d.rtx_id, 'value': _d.fullname}
        """
        # ---------------------- parameters check ----------------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_user_kv_list_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            v = str(v)
            new_params[k] = v
        # /////////// return data \\\\\\\\\\\\
        res, total = self.sysuser_bo.get_all(new_params, is_admin=True, is_del=True)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        new_res = list()
        for _d in res:
            if not _d: continue
            new_res.append({'key': _d.rtx_id, 'value': _d.fullname})
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

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

from deploy.config import AUTH_LIMIT, AUTH_NUM, \
    ADMIN, MENU_ONE_LEVEL, \
    USER_DEFAULT_AVATAR, USER_DEFAULT_PASSWORD, USER_DEFAULT_INTROD
from deploy.utils.utils import d2s, get_now, md5, check_length


class AuthorityService(object):
    """
    authority service
    """

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

    def __init__(self):
        """
        authority service class initialize
        """
        super(AuthorityService, self).__init__()
        self.role_bo = RoleBo()
        self.menu_bo = MenuBo()
        self.sysuser_bo = SysUserBo()

    def _role_model_to_dict(self, model):
        """
        role model to dict data
        return json data
        """
        if not model:
            return {}

        res = dict()
        for attr in self.role_list_attrs:
            if not attr:continue
            if attr == 'engname':
                res[attr] = model.engname
            elif attr == 'chnname':
                res[attr] = model.chnname
            elif attr == 'md5_id':
                res[attr] = model.md5_id
            elif attr == 'authority':
                res[attr] = model.authority
            elif attr == 'introduction':
                res[attr] = model.introduction or '' \
                    if len(model.introduction) < AUTH_NUM \
                    else '%s...查看详情' % str(model.introduction)[:AUTH_NUM-1]
            elif attr == 'create_time':
                if model.create_time and isinstance(model.create_time, str):
                    res[attr] = model.create_time
                elif model.create_time and isinstance(model.create_time, datetime.datetime):
                    res[attr] = d2s(model.create_time)
                else:
                    res[attr] = ''
            elif attr == 'create_rtx':
                res[attr] = model.create_rtx
            elif attr == 'delete_time':
                if model.delete_time and isinstance(model.delete_time, str):
                    res[attr] = model.delete_time
                elif model.delete_time and isinstance(model.delete_time, datetime.datetime):
                    res[attr] = d2s(model.delete_time)
                else:
                    res[attr] = ''
            elif attr == 'delete_rtx':
                res[attr] = model.delete_rtx
            elif attr == 'is_del':
                res[attr] = model.is_del
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
                _res[attr] = model.id
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'fullname':
                _res['name'] = model.fullname
            elif attr == 'password' and is_pass:
                _res[attr] = model.password
            elif attr == 'email':
                _res[attr] = model.email or ""
            elif attr == 'phone':
                _res[attr] = model.phone or ""
            elif attr == 'avatar':
                _res[attr] = model.avatar or USER_DEFAULT_AVATAR
            elif attr == 'introduction':
                if not is_detail:
                    _res[attr] = '%s...查看详情' % str(model.introduction)[0: AUTH_NUM-1] \
                        if model.introduction and len(model.introduction) > AUTH_NUM \
                        else model.introduction or ""
                else:
                    _res[attr] = model.introduction or ""
            elif attr == 'department':
                _res[attr] = model.department or ""
            elif attr == 'role':  # 多角色，存储role的engname，也就是role的rtx_id
                _res[attr] = str(model.role).split(';') if model.role else []
            elif attr == 'create_time':
                _res[attr] = d2s(model.create_time) \
                    if not isinstance(model.create_time, str) else model.create_time or ''
            elif attr == 'create_rtx':
                _res[attr] = model.create_rtx or ''
            elif attr == 'is_del':
                _res[attr] = True if model.is_del else False
            elif attr == 'delete_time':
                if not isinstance(model.delete_time, str):
                    _res[attr] = d2s(model.delete_time)
                elif isinstance(model.delete_time, str) and model.delete_time == '0000-00-00 00:00:00':
                    _res[attr] = ''
                else:
                    _res[attr] = model.delete_time or ''
            elif attr == 'delete_rtx':
                _res[attr] = model.delete_rtx or ""
        else:
            return _res

    def role_list(self, params):
        """
        get role list, many parameters
        return json data

        default get role is no delete
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

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

        res, total = self.role_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}
            ).json()
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._role_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def role_add(self, params):
        """
        add new role, information contain: english name, chinese name, introduction
        :return: json data

        new data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_role_add_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}
                ).json()
            # check: length
            if k == 'engname' and not check_length(v, 25):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'engname' and not check_length(v, 35):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'introduction' and not check_length(v, 55):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            new_params[k] = str(v)

        # check engname is or not repeat
        model = self.role_bo.get_model_by_engname(new_params.get('engname'))
        if model:
            return Status(
                213, 'failure', '角色RTX已存在，请重新输入', {}
            ).json()

        new_model = self.role_bo.new_mode()
        new_model.engname = new_params.get('engname')
        new_model.chnname = new_params.get('chnname')
        md5_id = md5(new_params.get('engname'))
        new_model.md5_id = md5_id
        new_model.authority = ''
        new_model.introduction = new_params.get('introduction')
        new_model.create_time = get_now()
        new_model.create_rtx = new_params.get('rtx_id')
        new_model.is_del = False
        self.role_bo.add_model(new_model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': md5_id}
        ).json()

    def role_update(self, params):
        """
        update role, information contain: chinese name, introduction
        by role md5
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_role_update_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}
                ).json()
            # check: length
            if k == 'engname' and not check_length(v, 25):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'engname' and not check_length(v, 35):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'introduction' and not check_length(v, 55):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            new_params[k] = str(v)

        if new_params.get('engname') == ADMIN:
            return Status(
                213, 'failure', u'AMDIN角色为系统默认角色，不允许操作', {}
            ).json()

        # check engname is or not repeat
        model = self.role_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在', {}
            ).json()
        # data is delete
        if model and model.is_del:
            return Status(
                304, 'failure', '数据已删除，不允许更新', {}
            ).json()

        model.chnname = new_params.get('chnname')
        model.introduction = new_params.get('introduction')
        self.role_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def role_batch_delete(self, params):
        """
        batch delete many role data, from role table
        post request and json parameters
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_role_deletes_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            if k == 'list':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)

        all_data = self.role_bo.get_models_by_md5list(new_params.get('list'))
        if not all_data:
            return Status(
                302, 'failure', u'请求删除数据不存在', {}
            ).json()
        for _d in all_data:
            if not _d: continue
            if _d.engname == ADMIN:
                return Status(
                    302, 'failure', u'Admin角色不允许操作，请重新选择', {}
                ).json()

        res = self.role_bo.batch_delete_by_md5(params=new_params)
        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure', StatusMsgs.get(303), {'success': res, 'failure': (len(new_params.get('list')) - res)}).json()

    def role_delete(self, params):
            """
            one delete many role data
            from role table
            post request and json parameters
            :return: json data
            """
            if not params:
                return Status(
                    212, 'failure', StatusMsgs.get(212), {}
                ).json()

            new_params = dict()
            for k, v in params.items():
                if not k: continue
                if k not in self.req_role_delete_attrs:
                    return Status(
                        213, 'failure', u'请求参数%s不合法' % k, {}
                    ).json()
                if not v:
                    return Status(
                        214, 'failure', u'请求参数%s不允许为空' % k, {}
                    ).json()
                new_params[k] = str(v)

            model = self.role_bo.get_model_by_md5(md5=new_params.get('md5'))
            # not exist
            if not model:
                return Status(
                    302, 'failure', StatusMsgs.get(302), {}
                ).json()
            # data is deleted
            if model and model.is_del:
                return Status(
                    306, 'failure', StatusMsgs.get(306), {}
                ).json()
            # authority
            rtx_id = new_params.get('rtx_id')
            if rtx_id != ADMIN and model.rtx_id != rtx_id:
                return Status(
                    311, 'failure', StatusMsgs.get(311), {}
                ).json()
            model.is_del = True
            model.delete_rtx = rtx_id
            model.delete_time = get_now()
            self.role_bo.merge_model(model)
            return Status(
                100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
            ).json()

    def role_auth_tere(self, params):
        """
        get the role authority list
        :return: json data
        authority is tree
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()
        if not params.get('md5'):
            return Status(
                214, 'failure', '缺少md5请求参数', {}
            ).json()

        role_model = self.role_bo.get_model_by_md5(
            md5=params.get('md5'))
        # not exist
        if not role_model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}
            ).json()
        # data is deleted
        if role_model and role_model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}
            ).json()
        # authority
        auths = str(role_model.authority).split(';') \
            if role_model.authority else []
        auth_list = [int(x) for x in auths if x]
        all_menus = self.menu_bo.get_all(root=False)
        # not menu data
        if not all_menus:
            return Status(
                101, 'failure', StatusMsgs.get(101), {}
            ).json()

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

        del template_list
        return Status(
            100, 'success', StatusMsgs.get(100),
            {"menus": _res, "auths": auth_list, "expand": auth_list}
        ).json()

    def role_save_tree(self, params):
        """
        save role authority from db table role
        authority is list type, data is keys
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_role_auth_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            if k == 'keys':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                new_v = [str(i) for i in v]
                v = ';'.join(new_v)
            new_params[k] = str(v)

        model = self.role_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}
            ).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}
            ).json()
        # authority
        model.authority = new_params.get('keys')
        self.role_bo.merge_model(model)
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

    def user_list(self, params):
        """
        get user list, many parameters: limit, offset
        return json data

        default get user is no delete
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_user_list_attrs and v:
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

        res, total = self.sysuser_bo.get_all(new_params, is_admin=False)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}
            ).json()
        new_res = list()
        for _d in res:
            if not _d: continue
            _res_dict = self._user_model_to_dict(_d)
            if _res_dict:
                new_res.append(_res_dict)
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def user_add(self, params):
        """
        add new user, information contain: rtx_id, name, phone,
        email, password, role, introduction
        add_rtx_id: 添加用户的账号rtx
        :return: json data

        new data:
        头像采用随机头像
        密码有个默认密码，在config中配置
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_user_add_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            # check: value is not null
            if not v and k not in ['password', 'email', 'introduction']:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}
                ).json()
            # check: length
            if k == 'rtx_id' and not check_length(v, 25):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'name' and not check_length(v, 30):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'phone' and len(v) != 11:
                return Status(
                    213, 'failure', u'正确电话为11位' % k, {}
                ).json()
            elif k == 'email' and not check_length(v, 35):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'introduction' and not check_length(v, 255):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            # check: role
            if k == 'role':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                # TODO 可以加上role验证
                new_params[k] = ';'.join(v)
            else:
                new_params[k] = str(v)

        # check rtx_id is or not exist
        model = self.sysuser_bo.get_user_by_rtx_id(new_params.get('rtx_id'))
        if model:
            return Status(
                213, 'failure', '用户RTX已存在，请重新输入', {}
            ).json()

        new_model = self.sysuser_bo.new_mode()
        new_model.rtx_id = new_params.get('rtx_id')
        new_model.fullname = new_params.get('name')
        md5_id = md5(new_params.get('rtx_id'))
        new_model.md5_id = md5_id
        new_model.password = new_params.get('password') or USER_DEFAULT_PASSWORD
        new_model.phone = new_params.get('phone') or ""
        new_model.email = new_params.get('email') or ""
        new_model.avatar = USER_DEFAULT_AVATAR
        new_model.department = ""
        new_model.role = new_params.get('role') or ""
        new_model.introduction = new_params.get('introduction') or USER_DEFAULT_INTROD
        new_model.create_time = get_now()
        new_model.create_rtx = new_params.get('add_rtx_id')
        new_model.is_del = False
        new_model.delete_time = ''
        self.role_bo.add_model(new_model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': md5_id}
        ).json()

    def user_batch_delete(self, params):
        """
        batch delete many user data, from sysuser table
        post request and json parameters
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_user_deletes_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            if k == 'list':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)

        all_data = self.sysuser_bo.get_models_by_md5_list(new_params.get('list'))
        if not all_data:
            return Status(
                302, 'failure', u'注销用户不存在', {}
            ).json()
        for _d in all_data:
            if not _d: continue
            if _d.rtx_id == ADMIN:
                return Status(
                    302, 'failure', u'Admin用户不允许注销，请重新选择', {}
                ).json()

        res = self.sysuser_bo.batch_delete_by_md5_list(params=new_params)
        return Status(100, 'success', '用户注销成功' or StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure', "成功：%s，失败：%s" % (res, (len(new_params.get('list')) - res)), {'success': res, 'failure': (len(new_params.get('list')) - res)}).json()

    def user_status(self, params):
        """
        one change user data status
        from user table
        post request and json parameters
        :return: json data

        状态改变：
        true：注销
        false：启用
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_user_status_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v and k != 'status':
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            if k == 'status':
                if not isinstance(v, bool):
                    return Status(
                        214, 'failure', u'请求参数%s类型不符合要求' % k, {}
                    ).json()
                new_params[k] = v
            else:
                new_params[k] = str(v)

        model = self.sysuser_bo.get_user_by_rtx_id(rtx_id=new_params.get('c_rtx_id'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '用户不存在' or StatusMsgs.get(302), {}
            ).json()
        # change status
        model.is_del = new_params.get('status')
        if new_params.get('status'):
            model.delete_rtx = new_params.get('rtx_id')
            model.delete_time = get_now()
        self.role_bo.merge_model(model)
        message = '用户注销成功' if new_params.get('status') else '用户启用成功'
        return Status(
            100, 'success', message or StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def user_info(self, params):
        """
        get user detail information
        by rtx id
        :return: json data

        data:
            - user base info
            - role list (select)
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        rtx_id = params.get('rtx_id')
        # check rtx_id is or not exist
        model = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        # not exist
        if not model:
            return Status(
                302, 'failure', '用户不存在' or StatusMsgs.get(302), {}
            ).json()
        # deleted: 先查看启用、注销2种状态的数据
        # if model and model.is_del:
        #     return Status(
        #         302, 'failure', '用户已注销' or StatusMsgs.get(302), {}
        #     ).json()

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
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_user_update_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            # check: value is not null
            if not v and k not in ['email', 'introduction']:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}
                ).json()
            # check: length
            if k == 'name' and not check_length(v, 30):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'phone' and len(v) != 11:
                return Status(
                    213, 'failure', u'正确电话为11位' % k, {}
                ).json()
            elif k == 'email' and not check_length(v, 35):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            elif k == 'introduction' and not check_length(v, 255):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()
            # check: role
            if k == 'role':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                # TODO 可以加上role验证
                new_params[k] = ';'.join(v)
            else:
                new_params[k] = str(v)

        model = self.sysuser_bo.get_user_by_rtx_id(new_params.get('to_rtx_id'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在', {}
            ).json()
        # data is delete: 注销 && 启用状态均可以更新
        # if model and model.is_del:
        #     return Status(
        #         304, 'failure', '数据已删除，不允许更新', {}
        #     ).json()

        model.fullname = new_params.get('name')
        model.phone = new_params.get('phone')
        model.email = new_params.get('email')
        model.role = new_params.get('role')
        model.introduction = new_params.get('introduction') or USER_DEFAULT_INTROD
        self.role_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {}
        ).json()

    def user_reset_pw(self, params):
        """
        reset user password
        default is abc1234
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        rtx_id = params.get('rtx_id')
        # check rtx_id is or not exist
        model = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        # not exist
        if not model:
            return Status(
                302, 'failure', '用户不存在' or StatusMsgs.get(302), {}
            ).json()
        # deleted
        if model and model.is_del:
            return Status(
                302, 'failure', '用户已注销' or StatusMsgs.get(302), {}
            ).json()

        # reset password
        model.password = USER_DEFAULT_PASSWORD
        self.role_bo.merge_model(model)

        return Status(
            100, 'success', StatusMsgs.get(100), {}
        ).json()

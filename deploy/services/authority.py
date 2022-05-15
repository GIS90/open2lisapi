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
from operator import itemgetter
from itertools import groupby

from deploy.utils.status_msg import StatusMsgs
from deploy.utils.status import Status
from deploy.bo.role import RoleBo
from deploy.bo.menu import MenuBo

from deploy.config import AUTH_LIMIT, AUTH_NUM, ADMIN, MENU_ONE_LEVEL
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

    def __init__(self):
        """
        authority service class initialize
        """
        super(AuthorityService, self).__init__()
        self.role_bo = RoleBo()
        self.menu_bo = MenuBo()

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
                    if len(model.introduction) < AUTH_NUM else '%s...查看详情' % str(model.introduction)[:AUTH_NUM-1]
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

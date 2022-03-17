# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/22 11:12 上午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "twtoolbox_isapi"

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
# usage: /usr/bin/python menu.py
# ------------------------------------------------------------
from operator import itemgetter
from itertools import groupby

from deploy.bo.menu import MenuBo
from deploy.utils.utils import d2s
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.config import MENU_ROOT_ID, MENU_ONE_LEVEL


class MenuService(object):
    def __init__(self):
        super(MenuService, self).__init__()
        self.menu_bo = MenuBo()
        self.all_attrs = [
            'id', 'name', 'path', 'title', 'pid', 'level', 'md5_id', 'component',
            'hidden', 'redirect', 'icon', 'noCache', 'affix', 'breadcrumb',
            'create_time', 'create_operator', 'is_del', 'del_time', 'del_operator'
        ]
        self.menu_attrs = [
            'id', 'name', 'path', 'pid', 'level', 'md5_id',
            'component', 'hidden', 'redirect',
        ]
        self.menu_meta_attrs = [
            'title', 'icon', 'noCache', 'affix', 'breadcrumb',
        ]
        self.del_attrs = [
            'id', 'pid', 'level', 'md5_id'
        ]

    def _model_to_menu_dict(self, model, level: int = 1) -> dict:
        if not model:
            return {}

        _res = dict()
        _meta = dict()
        for attr in (self.menu_attrs + self.menu_meta_attrs):
            if attr == 'id':
                _res[attr] = model.id or ""
            elif attr == 'name':
                _res[attr] = model.name or ""
            elif attr == 'path':
                _res[attr] = model.path or ""
            elif attr == 'title':
                _meta[attr] = model.title or ""
            elif attr == 'pid':
                _res[attr] = model.pid or ""
            elif attr == 'level':
                _res[attr] = model.level or ""
            elif attr == 'md5_id':
                _res[attr] = model.md5_id or ""
            elif attr == 'component':
                _res[attr] = model.component or ""
            elif attr == 'hidden':
                _res[attr] = True if model.hidden else False
            elif attr == 'redirect' and level == 1:
                _res[attr] = model.redirect or ""
            elif attr == 'icon':
                _meta[attr] = model.icon or ""
            elif attr == 'noCache' and level == 2:
                _meta[attr] = True if model.noCache else False
            elif attr == 'affix' and level == 2:
                _meta[attr] = True if model.affix else False
            elif attr == 'breadcrumb' and level == 2:
                _meta[attr] = True if model.breadcrumb else False
        else:
            _res['meta'] = _meta
            if level == 1:
                _res['alwaysShow'] = True
            return _res

    def _model_to_dict(self, model) -> dict:
        if not model:
            return {}

        _res = dict()
        for attr in self.all_attrs:
            if attr == 'id':
                _res[attr] = model.id or ""
            elif attr == 'name':
                _res[attr] = model.name or ""
            elif attr == 'path':
                _res[attr] = model.path or ""
            elif attr == 'title':
                _res[attr] = model.title or ""
            elif attr == 'pid':
                _res[attr] = model.pid or ""
            elif attr == 'level':
                _res[attr] = model.level or ""
            elif attr == 'md5_id':
                _res[attr] = model.md5_id or ""
            elif attr == 'component':
                _res[attr] = model.component or ""
            elif attr == 'hidden':
                _res[attr] = True if model.hidden else False
            elif attr == 'redirect':
                _res[attr] = model.redirect or ""
            elif attr == 'icon':
                _res[attr] = model.icon or ""
            elif attr == 'noCache':
                _res[attr] = True if model.noCache else False
            elif attr == 'affix':
                _res[attr] = True if model.affix else False
            elif attr == 'breadcrumb':
                _res[attr] = True if model.breadcrumb else False
            elif attr == 'create_time':
                _res[attr] = d2s(model.create_time) if model.create_time else ''
            elif attr == 'create_operator':
                _res[attr] = d2s(model.create_operator) or ''
            elif attr == 'is_del':
                _res[attr] = True if model.is_del else False
            elif attr == 'del_time':
                _res[attr] = d2s(model.del_time) if model.del_time else ''
            elif attr == 'del_operator':
                _res[attr] = model.del_operator or ""
        else:
            return _res

    def _del_nof_menu_d(self, menu: dict) -> dict:
        if not menu: return {}
        for attr in self.del_attrs:
            if not attr: continue
            del menu[attr]
        else:
            return menu

    def get_tree(self, auth_list: list, is_admin: bool = False) -> list:
        """
        思路：
            1.依据role中的authority值获取菜单数据
            2.每一条菜单数据转为字段类型数据的菜单
            3.把一级菜单加入one_menus，二级加入template_list
            4.对二级菜单进行分组
            5.把二级菜单加入对应的一级菜单的children
            6.return
        """
        if not auth_list and not is_admin:
            return []

        _res = list()
        all_menus = self.menu_bo.get_menus_by_ids(auth_list) \
            if not is_admin else self.menu_bo.get_all(root=False)
        if not all_menus:
            return _res

        template_list = list()
        one_menus = dict()
        for menu in all_menus:
            if not menu or menu.is_del or menu.hidden or \
                    not menu.name or not menu.path or \
                    not menu.component or not menu.level:
                continue
            _d = self._model_to_menu_dict(menu, level=menu.level)
            if not _d: continue
            one_menus[menu.id] = _d if menu.level == MENU_ONE_LEVEL \
                else template_list.append(_d)

        template_list.sort(key=itemgetter('pid'))
        for key, group in groupby(template_list, key=itemgetter('pid')):
            if key in one_menus.keys():
                _d = one_menus.get(key)
                # _d = self._del_nof_menu_d(_d)
                _d['children'] = list(group)
                _res.append(_d)

        del template_list
        return _res



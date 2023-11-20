# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    menu service

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/22 11:12 上午"
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
# usage: /usr/bin/python menu.py
# ------------------------------------------------------------
from operator import itemgetter
from itertools import groupby

from deploy.bo.menu import MenuBo
from deploy.utils.utils import d2s
from deploy.config import MENU_ROOT_ID, MENU_ONE_LEVEL


class MenuService(object):
    """
    menu service
    """

    all_attrs = [
        'id', 'name', 'path', 'title', 'pid', 'level', 'md5_id', 'component',
        'hidden', 'redirect', 'icon', 'noCache', 'affix', 'breadcrumb',
        'create_time', 'create_rtx', 'is_del', 'delete_time', 'delete_rtx'
    ]

    menu_attrs = [
        'id',
        'name',
        'path',
        'pid',
        'level',
        'md5_id',
        'component',
        'hidden',
        'redirect',
        'order_id'
    ]

    menu_meta_attrs = [
        'title',
        'icon',
        'cache',
        'affix',
        'breadcrumb',
    ]

    del_attrs = [
        'id',
        'pid',
        'level',
        'md5_id'
    ]

    def __init__(self):
        """
        MenuService class initialize
        """
        super(MenuService, self).__init__()
        # bo
        self.menu_bo = MenuBo()

    def __str__(self):
        print("MenuService class")

    def __repr__(self):
        self.__str__()

    def _model_to_menu_dict(self, model, level: int = 1) -> dict:
        """
        format menu model to dict type data
        return dict object

        格式化菜单对象
        """
        if not model:
            return {}

        _res = dict()
        _meta = dict()
        for attr in (self.menu_attrs + self.menu_meta_attrs):
            if attr == 'id':
                _res[attr] = model.id
            elif attr == 'name':
                _res[attr] = model.name
            elif attr == 'path':
                _res[attr] = model.path
            elif attr == 'title':
                _meta[attr] = model.title
            elif attr == 'pid':
                _res[attr] = model.pid
            elif attr == 'level':
                _res[attr] = model.level
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'order_id':
                _res[attr] = model.order_id
            elif attr == 'component':
                _res[attr] = model.component
            elif attr == 'hidden':
                _res[attr] = True if model.hidden else False
            elif attr == 'redirect' and level == 1:
                _res[attr] = model.redirect or ""
            elif attr == 'icon':
                _meta[attr] = model.icon or ""
            elif attr == 'cache' and level == 2:
                _meta[attr] = False if model.cache else True
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
                _res[attr] = model.level
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'order_id':
                _res[attr] = model.order_id
            elif attr == 'component':
                _res[attr] = model.component
            elif attr == 'hidden':
                _res[attr] = True if model.hidden else False
            elif attr == 'redirect':
                _res[attr] = model.redirect or ""
            elif attr == 'icon':
                _res[attr] = model.icon or ""
            elif attr == 'cache':
                _res[attr] = False if model.cache else True
            elif attr == 'affix':
                _res[attr] = True if model.affix else False
            elif attr == 'breadcrumb':
                _res[attr] = True if model.breadcrumb else False
            elif attr == 'create_time':
                _res[attr] = d2s(model.create_time) if model.create_time else ''
            elif attr == 'create_rtx':
                _res[attr] = d2s(model.create_rtx) or ''
            elif attr == 'is_del':
                _res[attr] = True if model.is_del else False
            elif attr == 'delete_time':
                _res[attr] = d2s(model.delete_time) if model.delete_time else ''
            elif attr == 'delete_rtx':
                _res[attr] = model.delete_rtx or ""
        else:
            return _res

    def _del_nof_menu_d(self, menu: dict) -> dict:
        if not menu: return {}
        for attr in self.del_attrs:
            if not attr: continue
            del menu[attr]
        else:
            return menu

    def get_routes(self, auth_list: list, is_admin: bool = False) -> list:
        """
        get user routers by authority list
        get_login_auth_by_rtx to use
        思路：
            1.get_all获取全部权限数据[去掉home根菜单]
            2.每一条菜单数据转为字段类型数据的菜单
            3.把一级菜单加入one_menus，二级加入template_list
            4.对二级菜单进行分组
            5.依据authority值对菜单进行判定
            5.把二级菜单加入对应的一级菜单的children
            6.return data

        获取用户菜单权限routers
        """
        if not auth_list and not is_admin:
            return []

        _res = list()
        all_menus = self.menu_bo.get_all(root=False)
        if not all_menus:
            return _res

        two_m_template_list = list()  # 二级临时菜单，List格式
        one_menus = dict()      # 一级菜单，Dict格式
        add_flag = dict()       # 是否添加router标志，Dict格式
        for menu in all_menus:
            if not menu or menu.is_del or menu.hidden or \
                    not menu.name or not menu.path or \
                    not menu.component or not menu.level:
                continue
            _d = self._model_to_menu_dict(menu, level=menu.level)
            if not _d: continue
            if is_admin:
                # 管理员特殊权限
                """TODO 后续优化只有一级、二级菜单功能"""
                if menu.level == 2:
                    add_flag[menu.pid] = True
                if menu.level == MENU_ONE_LEVEL:
                    one_menus[menu.id] = _d
                else:
                    two_m_template_list.append(_d)
                """fix bug: 处理one_menus二级空值问题"""
                # one_menus[menu.id] = _d if menu.level == MENU_ONE_LEVEL \
                #     else two_m_template_list.append(_d)
            else:
                # 非管理员，用二级菜单去判断是否有一级
                if menu.level == MENU_ONE_LEVEL:
                    one_menus[menu.id] = _d
                # auth_list 用户权限列表（非管理员的权限判断）
                if menu.level == 2 and menu.id in auth_list:
                    add_flag[menu.pid] = True
                    two_m_template_list.append(_d)

        two_m_template_list.sort(key=itemgetter('pid'))
        for key, group in groupby(two_m_template_list, key=itemgetter('pid')):
            if key in one_menus.keys() and add_flag.get(key):
                _d = one_menus.get(key)
                # _d = self._del_nof_menu_d(_d)
                _sort_group = sorted(group, key=itemgetter('order_id'), reverse=False)
                _d['children'] = list(_sort_group)
                _res.append(_d)

        del two_m_template_list
        # 一级菜单排序
        _sort_res = sorted(_res, key=itemgetter('order_id'), reverse=False)
        return _sort_res

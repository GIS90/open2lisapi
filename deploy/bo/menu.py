# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/22 11:08 上午"
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
from sqlalchemy import or_

from deploy.bo.bo_base import BOBase
from deploy.models.menu import MenuModel
from deploy.config import MENU_ROOT_ID, MENU_ONE_LEVEL


class MenuBo(BOBase):

    def __init__(self):
        super(MenuBo, self).__init__()

    def new_mode(self):
        return MenuModel()

    def get_all(self, root=False):
        q = self.session.query(MenuModel)
        if not root:
            q = q.filter(MenuModel.id != MENU_ROOT_ID)
        q = q.filter(MenuModel.is_del != True)
        q = q.order_by(MenuModel.order_id.asc(), MenuModel.id.asc())
        q = q.all()
        return q

    def get_all_no(self, root=False):
        q = self.session.query(MenuModel)
        if not root:
            q = q.filter(MenuModel.id != MENU_ROOT_ID)
        q = q.order_by(MenuModel.order_id.asc(), MenuModel.id.asc())
        q = q.all()
        return q

    def get_menus_by_ids(self, menu_ids):
        q = self.session.query(MenuModel)
        q = q.filter(MenuModel.id.in_(menu_ids))
        q = q.filter(MenuModel.is_del != True)
        q = q.order_by(MenuModel.order_id.asc(), MenuModel.id.asc())
        q = q.all()
        return q

    def get_model_by_md5(self, md5):
        q = self.session.query(MenuModel)
        q = q.filter(MenuModel.md5_id == md5)
        q = q.first()
        return q

    def get_root_one_menus(self):
        q = self.session.query(MenuModel)
        q = q.filter(MenuModel.level.in_([MENU_ROOT_ID, MENU_ONE_LEVEL]))
        q = q.order_by(MenuModel.order_id.asc(), MenuModel.id.asc())
        q = q.all()
        return q

    def get_model_by_name(self, name):
        q = self.session.query(MenuModel)
        q = q.filter(MenuModel.name == name)
        q = q.first()
        return q
# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    the base class of query db

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
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

from deploy.models.base import get_session


class BOBase(object):

    def __init__(self, model=None):
        self.session = get_session()
        self.model = model

    def get_model(self):
        return self.model

    def save_model(self):
        with self.session.begin():
            self.session.add(self.model)

    def merge_model(self, model):
        with self.session.begin():
            self.session.merge(model)

    def add_model(self, model):
        with self.session.begin():
            self.session.add(model)

    def merge_model_no_trans(self, model):
        self.session.merge(model)







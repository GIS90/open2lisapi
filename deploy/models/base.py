# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    the class of base model
    db connection session

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
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from deploy.config import DB_LINK
from deploy.utils.logger import logger as LOG

DBSession = None


if not DB_LINK:
    LOG.critical('DB configuration is unavail')
    sys.exit(1)

db_link = DB_LINK

ModelBase = declarative_base()


def init_database_engine():
    return create_engine(
        db_link,
        echo=False,
        pool_recycle=800,
        pool_size=100
    )


def get_session():
    global DBSession
    if not DBSession:
        dbengine_databus = init_database_engine()
        DBSession = sessionmaker(bind=dbengine_databus,
                                 autocommit=True
                                 )
    return DBSession()


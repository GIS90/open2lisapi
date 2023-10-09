# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    the entry point of system
    use gunicorn to start project(gunicorn -c etc/dev/gunicorn.conf wsgi:app)
    or directly execute  the file to start(python wsgi.py)
    python version: python3

    Enjoy the good life everyday！！!

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
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
# usage: /usr/bin/python wsgi.py
# ------------------------------------------------------------
from deploy import create_app

app = create_app()

# 手动启动
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9999, debug=True)

# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    the request http lib

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/8/4 4:35 PM"
    __mail__ = "gaoming971366@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python http.py
# ------------------------------------------------------------

import requests
import json
import time
import random
from requests.auth import HTTPBasicAuth
from deploy.utils.logger import logger as LOG
import urllib3

urllib3.disable_warnings()


class HttpLibApi(object):
    def __init__(self, root, username='', password='', headers=None,
                 is_try=3, timeout=120):
        self.root = root
        self.auth = HTTPBasicAuth(username, password)
        self.content_type_form = {
            'Content-type': 'application/x-www-form-urlencoded'}
        self.content_type_json = {
            'Content-type': 'application/json'}
        self.headers = headers
        self.is_try = is_try
        self.timeout = timeout

    def _wrap_headers(self, headers, ctype='form'):
        _headers = {}
        if self.headers:
            _headers.update(self.headers)
        _headers.update(headers or {})
        content_type = 'application/x-www-form-urlencoded' if ctype == 'form' \
            else 'application/json;charset=utf-8'
        _headers.update({
            'Content-type': content_type
        })
        return _headers

    def _get(self, url, params=None, headers=None, ctype='form', resptype='json', **kwargs):
        headers = self._wrap_headers(headers, ctype=ctype)
        url = '%s%s' % (self.root, url)
        params = params if params else {}
        try:
            response = requests.get(
                url, headers=headers, params=params, timeout=self.timeout, **kwargs)
        except Exception as e:
            LOG.error(u'HTTPLIB %s api_get error: %s' % (url, e))
            return False, []
        respcode = response.status_code
        if respcode != 200:
            return False, 'api_get response status code is: %s' % respcode
        elif respcode == 200 and resptype == 'raw':
            return True, response.raw
        elif respcode == 200 and resptype == 'content':
            return True, response.content
        elif respcode == 200 and resptype == 'json':
            return True, response.json()
        else:
            return True, response.text

    def _post(self, url, headers=None, data=None, params=None, resptype='json',
              ctype='form', **kwargs):
        url = '%s%s' % (self.root, url)
        headers = self._wrap_headers(headers, ctype=ctype)
        params = params if params else {}
        data = data if data else {}
        if ctype == 'json':
            data = json.dumps(data)
        try:
            response = requests.post(
                url, headers=headers, params=params, data=data, timeout=self.timeout,
                verify=False, **kwargs)
        except Exception as e:
            LOG.error(u'HTTPLIB %s api_post error: %s' % (url, e))
            return False, []
        respcode = response.status_code
        if respcode != 200:
            return False, 'api_post response status code is: %s' % respcode
        elif respcode == 200 and resptype == 'raw':
            return True, response.raw
        elif respcode == 200 and resptype == 'content':
            return True, response.content
        elif respcode == 200 and resptype == 'json':
            return True, response.json()
        else:
            return True, response.text

    def _put(self, url, headers=None, data=None, params=None, resptype='json',
              ctype='form', **kwargs):
        url = '%s%s' % (self.root, url)
        headers = self._wrap_headers(headers, ctype=ctype)
        params = params if params else {}
        data = data if data else {}
        if ctype == 'json':
            data = json.dumps(data)
        try:
            response = requests.put(
                url, headers=headers, params=params, data=data, timeout=self.timeout,
                verify=False, **kwargs)
        except Exception as e:
            LOG.error(u'HTTPLIB %s api_put error: %s' % (url, e))
            return False, []
        respcode = response.status_code
        if respcode != 200:
            return False, 'api_put response status code is: %s' % respcode
        elif respcode == 200 and resptype == 'raw':
            return True, response.raw
        elif respcode == 200 and resptype == 'content':
            return True, response.content
        elif respcode == 200 and resptype == 'json':
            return True, response.json()
        else:
            return True, response.text

    def get_form(self, url, *args, **kwargs):
        return self._get(url, *args, **dict(kwargs, **{'ctype': 'form'}))

    def get_json(self, url, *args, **kwargs):
        return self._get(url, *args, **dict(kwargs, **{'ctype': 'json'}))

    def post_form(self, url, *args, **kwargs):
        return self._post(url, *args, **dict(kwargs, **{'ctype': 'form'}))

    def post_json(self, url, *args, **kwargs):
        return self._post(url, *args, **dict(kwargs, **{'ctype': 'json'}))

    def put_form(self, url, *args, **kwargs):
        return self._put(url, *args, **dict(kwargs, **{'ctype': 'form'}))

    def put_json(self, url, *args, **kwargs):
        return self._put(url, *args, **dict(kwargs, **{'ctype': 'json'}))

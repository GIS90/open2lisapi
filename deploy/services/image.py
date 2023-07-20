# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2023/7/20 23:23"
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
# usage: /usr/bin/python image.py
# ------------------------------------------------------------
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs


class ImageService(object):
    """
    image service
    """

    PAGE_LIMIT = 15

    # 用户
    req_user_necessary_attrs = ['rtx_id']

    # 数据md5
    req_md5_necessary_attrs = ['rtx_id', 'md5']

    # list api
    req_list_necessary_attrs = ['rtx_id', 'limit', 'offset']

    # define many request api parameters
    # 分页数据通用请求参数
    req_page_comm_attrs = [
        'rtx_id',
        'limit',
        'offset'
    ]

    def avatar_list(self, params: dict) -> dict:
        """
        get avatar data list by params
        params is dict
        return json data
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_page_comm_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_page_comm_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if k == 'limit':
                v = int(v) if v else self.PAGE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            else:
                v = str(v) if v else ''
            new_params[k] = v

        images = [
            {'id': 1, 'url': "http://2lstore.pygo2.top/avatars/1a02dfe1808eaadc5e9c8d70f5733daa.jpeg"},
            {'id': 2, 'url': 'http://2lstore.pygo2.top/avatars/2fbdcfae592accd03f6c0170b288e985.jpeg'},
            {'id': 3, 'url': 'http://2lstore.pygo2.top/avatars/3c87f0f3cc5af848c32d80ca05f24542.jpeg'},
            {'id': 4, 'url': 'http://2lstore.pygo2.top/avatars/4f6162b0284b95fa699e17f8e6f5929d.jpeg'},
            {'id': 5, 'url': 'http://2lstore.pygo2.top/avatars/5d9b1e6862029fce98b342e2a1b727be.jpeg'},
            {'id': 6, 'url': 'http://2lstore.pygo2.top/avatars/f6203911630ee1b04db542c02629b25b.jpeg'},
            {'id': 7, 'url': 'http://2lstore.pygo2.top/avatars/4336fa14f3f2a6c075395fad6d631611.jpeg'},
            {'id': 8, 'url': 'http://2lstore.pygo2.top/avatars/b7cbcdc96f20fdf497c4d3d4f5a0dbc2.jpeg'},
            {'id': 9, 'url': 'http://2lstore.pygo2.top/avatars/c933509f3fcc721e6f8e8612f7ec8725.jpeg'},
            {'id': 10, 'url': 'http://2lstore.pygo2.top/avatars/cf54984fcab697eed7df219d5128cda0.jpeg'},
            {'id': 11, 'url': 'http://2lstore.pygo2.top/avatars/d65d529de6fb7a186d07e3920767307a.jpeg'},
            {'id': 12, 'url': 'http://2lstore.pygo2.top/avatars/e3471b6c8b2806548eae9d4b4a22d596.jpeg'},
            {'id': 13, 'url': 'http://2lstore.pygo2.top/avatars/f0cfc6c28eb2cee49f3c65130c28868e.jpeg'},
            {'id': 14, 'url': 'http://2lstore.pygo2.top/avatars/f71b2efcb9b12fc50d4fe91174291430.jpeg'},
            {'id': 15, 'url': 'http://2lstore.pygo2.top/avatars/4336fa14f3f2a6c075395fad6d631611.jpeg'},
            {'id': 16, 'url': 'http://2lstore.pygo2.top/avatars/b7cbcdc96f20fdf497c4d3d4f5a0dbc2.jpeg'},
            {'id': 17, 'url': 'http://2lstore.pygo2.top/avatars/c933509f3fcc721e6f8e8612f7ec8725.jpeg'},
            {'id': 18, 'url': 'http://2lstore.pygo2.top/avatars/cf54984fcab697eed7df219d5128cda0.jpeg'},
            {'id': 19, 'url': 'http://2lstore.pygo2.top/avatars/d65d529de6fb7a186d07e3920767307a.jpeg'},
            {'id': 20, 'url': 'http://2lstore.pygo2.top/avatars/e3471b6c8b2806548eae9d4b4a22d596.jpeg'},
            {'id': 21, 'url': 'http://2lstore.pygo2.top/avatars/f0cfc6c28eb2cee49f3c65130c28868e.jpeg'}
        ]
        return Status(
            100, 'failure', StatusMsgs.get(100), {'list': images, 'total': 21}).json()

        """
        # **************** <get data> *****************
        res, total = self.enum_bo.get_all(new_params)
        # no data
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # <<<<<<<<<<<<<<<<<<<< format and return data >>>>>>>>>>>>>>>>>>>>
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._enum_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()
        """

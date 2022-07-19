# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/7/18 21:16"
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
# usage: /usr/bin/python notify.py
# ------------------------------------------------------------
import os
import json

from deploy.utils.excel_lib import ExcelLib
from deploy.utils.utils import get_now, d2s
from deploy.bo.dtalk_message import DtalkMessageBo
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.config import OFFICE_LIMIT, SHEET_NUM_LIMIT, SHEET_NAME_LIMIT, \
    STORE_BASE_URL, STORE_SPACE_NAME
from deploy.utils.store_lib import StoreLib


class NotifyService(object):
    """
    notify service
    """

    # define many request api parameters
    req_dtalk_list_attrs = [
        'rtx_id',
        'limit',
        'offset'
    ]

    req_upload_attrs = [
        'rtx_id',
        'file_type',
        'excel_sub_type'
    ]

    dtalk_show_attrs = [
        'id',
        'rtx_id',
        'name',    # file_name
        'url',  # 'file_local_url', 'file_store_url',
        'md5_id',
        'robot',
        'count',
        'number',
        'nsheet',
        'sheet_names',
        'sheet_columns',
        'headers',
        'set_sheet',
        'title',
        'create_time',
        'delete_rtx',
        'delete_time',
        'is_del'
    ]

    def __init__(self):
        """
        common service class initialize
        """
        super(NotifyService, self).__init__()
        self.excel_lib = ExcelLib()
        self.store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)
        self.dtalk_bo = DtalkMessageBo()

    def get_excel_headers(self, excel_file):
        """
        get excel base information
        contain:
            - sheet names
            - number sheet
            - sheet columns

        get information from excel lib(deploy/utils/excel_lib.py)
        """
        res = {'sheets': {}, 'nsheet': 0, 'names': {}, 'columns': {}}
        if not excel_file or not os.path.exists(excel_file):
            return res
        new_res = self.excel_lib.read_headers(excel_file)
        return new_res

    def store_dtalk_to_db(self, store):
        """
        store dtalk excel source file message to db
        params store: store message
            - rtx_id: rtx-id
            - file_type: file type
            - excel_sub_type: excel opr type, merge or split
            - name: file name
            - md5: file md5
            - store_name: file store name
            - path: file store url, no have store base url
            - message: message

        default value:
            - count: count operation, default value is 0
            - number: send number operation, default value is 0
            - set_sheet: operation sheet index, default value is 0

        excel headers from excel_lib get_headers methods

        robot默认为空
        """
        if not store:
            return False

        try:
            # 获取文件header
            excel_headers = self.get_excel_headers(store.get('path'))
            # create new mode
            new_model = self.dtalk_bo.new_mode()
            new_model.rtx_id = store.get('rtx_id')
            new_model.file_name = store.get('name')
            new_model.file_local_url = store.get('path')
            new_model.file_store_url = store.get('store_name')
            new_model.md5_id = store.get('md5')
            new_model.count = 0
            new_model.number = 0
            new_model.nsheet = excel_headers.get('nsheet')
            # 设置默认第一个Sheet进行操作,初始化设置
            new_model.set_sheet = '0'
            new_model.sheet_names = json.dumps(excel_headers.get('names'))
            new_model.sheet_columns = json.dumps(excel_headers.get('columns'))
            new_model.headers = json.dumps(excel_headers.get('sheets'))
            new_model.create_time = get_now()
            new_model.is_del = False
            self.dtalk_bo.add_model(new_model)
            return True
        except:
            return False

    def _dtalk_model_to_dict(self, model):
        """
        dtalk model to dict
        params model: dtalk model object
        attrs from class define attrs
        return dict data
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.dtalk_show_attrs:
            if not attr: continue
            if attr == 'id':
                _res[attr] = model.id
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id
            elif attr == 'name':
                _res[attr] = model.file_name
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'robot':
                _res[attr] = model.robot
            elif attr == 'count':
                _res[attr] = model.count or 0
            elif attr == 'number':
                _res[attr] = model.number or 0
            elif attr == 'url':
                if model.file_store_url:
                    # 直接拼接的下载url，无check ping
                    _res['url'] = self.store_lib.open_download_url(store_name=model.file_store_url)
                    # url and check ping
                    # resp = self.store_lib.open_download(store_name=model.store_url)
                    # _res['url'] = resp.get('data').get('url') if resp.get('status_id') == 100 else ''
                else:
                    _res['url'] = ''
            elif attr == 'nsheet':
                _res['nsheet'] = model.nsheet if model.nsheet else 1  # 无值，默认为1个SHEET
            elif attr == 'set_sheet':
                if model.sheet_names:
                    new_res = list()
                    set_sheet_name = list()
                    set_sheet_index = [str(i) for i in str(model.set_sheet).split(';')] if model.set_sheet else ['0']  # 默认index为0
                    for k, v in json.loads(model.sheet_names).items():
                        new_res.append({'key': k, 'value': v})
                        if str(k) in set_sheet_index:
                            set_sheet_name.append(v)
                        if int(k) >= SHEET_NUM_LIMIT:  # 加了展示条数的限制，否则页面展示太多
                            new_res.append({'key': '...N', 'value': '（具体查看请下载）'})
                            break
                    _res['sheet_names'] = new_res
                    set_sheet_name = ';'.join(set_sheet_name)
                    if len(set_sheet_name) > SHEET_NAME_LIMIT:  # 加了展示字数的限制，否则页面展示太多
                        set_sheet_name = '%s...具体查看请下载' % set_sheet_name[0:SHEET_NAME_LIMIT]
                    _res['set_sheet_name'] = set_sheet_name
                    _res['set_sheet_index'] = set_sheet_index
                else:
                    _res['sheet_names'] = []
                    _res['set_sheet_index'] = []
                    _res['set_sheet_name'] = ''
            elif attr == 'title':
                _res[attr] = model.title or ""
            elif attr == 'create_time':
                _res['create_time'] = d2s(model.create_time) if model.create_time else ''
        else:
            return _res

    def dtalk_list(self, params):
        """
        get dtalk list by params
        params is dict
        return json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_dtalk_list_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if k == 'limit':
                v = int(v) if v else OFFICE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            else:
                v = str(v) if v else ''
            new_params[k] = v

        res, total = self.dtalk_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}
            ).json()

        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._dtalk_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

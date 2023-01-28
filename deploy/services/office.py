# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    office service

base_info:
    __author__ = "PyGo"
    __time__ = "2022/4/25 11:31 下午"
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
# usage: /usr/bin/python excel.py
# ------------------------------------------------------------
import os
import json
import datetime
from operator import itemgetter
from itertools import groupby

from deploy.utils.status_msg import StatusMsgs
from deploy.utils.status import Status
from deploy.delibs.file_lib import FileLib
from deploy.delibs.store_lib import StoreLib
from deploy.delibs.excel_lib import ExcelLib
from deploy.bo.excel_source import ExcelSourceBo
from deploy.bo.excel_result import ExcelResultBo
from deploy.bo.enum import EnumBo
from deploy.bo.office_pdf import OfficePDFBo

from deploy.config import STORE_BASE_URL, STORE_SPACE_NAME, \
    OFFICE_LIMIT, OFFICE_STORE_BK, \
    ADMIN, ADMIN_AUTH_LIST, SHEET_NAME_LIMIT, SHEET_NUM_LIMIT
from deploy.utils.utils import get_now, d2s, md5, check_length, auth_rtx_join
from deploy.utils.enums import *


class OfficeService(object):
    """
    office service
    """

    # define many request api parameters
    req_source_list_attrs = [
        'rtx_id',
        'type',
        'limit',
        'offset'
    ]

    req_result_list_attrs = [
        'rtx_id',
        'name',
        'type',
        'start_time',
        'end_time',
        'limit',
        'offset'
    ]

    req_upload_attrs = [
        'rtx_id',
        'file_type',
        'excel_sub_type'
    ]

    req_source_update_attrs = [
        'rtx_id',
        'name',
        'md5',
        'set_sheet'
    ]

    req_result_update_attrs = [
        'rtx_id',
        'name',
        'md5'
    ]

    req_detail_attrs = [
        'rtx_id',
        'md5'
    ]

    req_delete_attrs = [
        'rtx_id',
        'md5'
    ]

    req_deletes_attrs = [
        'rtx_id',
        'list'
    ]

    req_merge_attrs = [
        'rtx_id',
        'name',
        'list',
        'blank'
    ]

    req_init_split_attrs = [
        'rtx_id',
        'md5'
    ]

    req_sheet_header_attrs = [
        'rtx_id',
        'md5',
        'sheet'
    ]

    req_split_attrs = [
        'rtx_id',
        'md5',
        'name',
        'sheet',
        'store',
        'split',
        'columns',
        'header'
    ]

    excel_source_all_attrs = [
        'id',
        'name',
        'store_name',
        'md5_id',
        'rtx_id',
        'ftype',
        'local_url',
        'store_url',
        'nsheet',
        'set_sheet',
        'sheet_names',
        'sheet_columns',
        'headers',
        'create_time',
        'delete_rtx',
        'delete_time',
        'is_del'
    ]

    excel_source_show_attrs = [
        'id',
        'name',
        'md5_id',
        'rtx_id',
        'ftypek',
        'ftypev',
        'url',
        'numopr',
        'nsheet',
        'set_sheet',  # sheet_names: sheet列表名称集合，[{'key': k, 'value': v}]格式
                      # set_sheet_index: 选择sheet列表index索引值集合，[]格式
                      # set_sheet_name: 选择sheet列表名称，string类型（；分割）
        # 'sheet_columns',
        'create_time',
        # 'delete_rtx',
        # 'delete_time',
        'is_del'
    ]

    excel_result_show_attrs = [
        'id',
        'name',
        'md5_id',
        'rtx_id',
        'ftypek',
        'ftypev',
        'url',
        'compress',
        'nfile',
        'nsheet',
        'row',
        'col',
        'set_sheet',  # sheet_names Sheet名称列表（key value格式）
                      # set_sheet_name 全部的Sheet名称，string类型（；分割）
        'create_time',
        # 'delete_rtx',
        # 'delete_time',
        'is_del'
    ]

    req_pdf2word_list_attrs = [
        'rtx_id',
        'limit',
        'offset'
    ]

    office_pdf_show_attrs = [
        'id',
        'name',
        'store_name',
        'transfer_name',
        'md5_id',
        'rtx_id',
        'file_type',
        'transfer',
        'transfer_time',
        'local_url',
        'store_url',
        'transfer_url',
        'mode',
        'start',
        'end',
        'pages',
        'create_time',
        'delete_rtx',
        'delete_time',
        'is_del'
    ]

    req_pdf_update_attrs = [
        'rtx_id',
        'start',
        'end',
        'pages',
        'mode',
        'md5'
    ]

    req_pdf_convert_attrs = [
        'rtx_id',
        'name',
        'start',
        'end',
        'pages',
        'mode',
        'md5'
    ]

    req_pdf_convert_need_attrs = [
        'rtx_id',
        'name',
        'md5'
    ]

    EXCEL_FORMAT = ['.xls', '.xlsx']

    DEFAULT_EXCEL_FORMAT = '.xlsx'

    def __init__(self):
        """
        office service class initialize
        """
        super(OfficeService, self).__init__()
        self.excel_lib = ExcelLib()
        self.file_lib = FileLib()
        self.store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)
        self.excel_source_bo = ExcelSourceBo()
        self.excel_result_bo = ExcelResultBo()
        self.enum_bo = EnumBo()
        self.office_pdf_bo = OfficePDFBo()

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
        if not excel_file \
                or not os.path.exists(excel_file):
            return res
        new_res = self.excel_lib.read_headers(excel_file)
        return new_res

    def store_office_pdf_to_db(self, store):
        """
        store office pdf file message to db
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
            - numopr: number operation, default value is 0
            - set_sheet: operation sheet index, default value is 0

        excel headers from excel_lib get_headers methods
        """
        if not store:
            return False

        try:
            # create new mode
            new_model = self.office_pdf_bo.new_mode()
            new_model.rtx_id = store.get('rtx_id')
            new_model.name = store.get('name')
            new_model.store_name = store.get('store_name')
            new_model.md5_id = store.get('md5')
            new_model.file_type = store.get('file_type')
            new_model.transfer = False
            new_model.local_url = store.get('path')
            new_model.store_url = store.get('store_name')
            new_model.create_time = get_now()
            new_model.mode = True
            new_model.is_del = False
            self.office_pdf_bo.add_model(new_model)
            return True
        except:
            return False

    def store_excel_source_to_db(self, store):
        """
        store excel source file message to db
        params store: store message
            - rtx_id: rtx-id
            - file_type: file type, excel opr type, merge or split
            - name: file name
            - md5: file md5
            - store_name: file store name
            - path: file store url, no have store base url
            - message: message

        default value:
            - numopr: number operation, default value is 0
            - set_sheet: operation sheet index, default value is 0

        excel headers from excel_lib get_headers methods
        """
        if not store:
            return False

        try:
            # 获取文件header
            excel_headers = self.get_excel_headers(store.get('path'))
            # create new mode
            new_model = self.excel_source_bo.new_mode()
            new_model.rtx_id = store.get('rtx_id')
            new_model.name = store.get('name')
            new_model.store_name = store.get('store_name')
            new_model.md5_id = store.get('md5')
            new_model.ftype = store.get('file_type')
            new_model.local_url = store.get('path')
            new_model.store_url = store.get('store_name')
            new_model.numopr = 0
            new_model.nsheet = excel_headers.get('nsheet')
            # 设置默认第一个Sheet进行操作,初始化设置
            new_model.set_sheet = '0'
            new_model.sheet_names = json.dumps(excel_headers.get('names'))
            new_model.sheet_columns = json.dumps(excel_headers.get('columns'))
            new_model.headers = json.dumps(excel_headers.get('sheets'))
            new_model.create_time = get_now()
            new_model.is_del = False
            self.excel_source_bo.add_model(new_model)
            return True
        except:
            return False

    def store_excel_result_to_db(self, store):
        """
        store excel result file message to db
        params store: store message
            - rtx_id: rtx-id
            - type: excel opr type
            - name: file name
            - md5: file md5
            - store_name: file store name
            - path: file store url, no have store base url
            - message: message
            - compress: is or not compress file format
            - nfile: number file

        excel headers from excel_lib get_headers methods
        """
        if not store:
            return False

        is_compress = store.get('compress') or False
        try:
            # 获取文件header
            excel_headers = self.get_excel_headers(store.get('path')) \
                if not is_compress else {}

            new_model = self.excel_result_bo.new_mode()
            new_model.rtx_id = store.get('rtx_id')
            new_model.name = store.get('name')
            new_model.store_name = store.get('store_name')
            new_model.md5_id = store.get('md5')
            new_model.ftype = store.get('type')
            new_model.local_url = store.get('path')
            new_model.store_url = store.get('store_name')
            new_model.nfile = store.get('nfile') or 1
            new_model.is_compress = is_compress
            new_model.row = excel_headers.get('sheets').get('0').get('row') \
                if (int(store.get('type')) == int(FileTypeEnum.EXCEL_MERGE.value) or not is_compress) and excel_headers else 0
            new_model.col = excel_headers.get('sheets').get('0').get('col') \
                if (int(store.get('type')) == int(FileTypeEnum.EXCEL_MERGE.value) or not is_compress) and excel_headers else 0
            new_model.nsheet = excel_headers.get('nsheet') \
                if (int(store.get('type')) == int(FileTypeEnum.EXCEL_MERGE.value) or not is_compress) and excel_headers else 0
            new_model.sheet_names = json.dumps(excel_headers.get('names')) \
                if (int(store.get('type')) == int(FileTypeEnum.EXCEL_MERGE.value) or not is_compress) and excel_headers else '{}'
            new_model.sheet_columns = json.dumps(excel_headers.get('columns')) \
                if (int(store.get('type')) == int(FileTypeEnum.EXCEL_MERGE.value) or not is_compress) and excel_headers else '{}'
            new_model.headers = json.dumps(excel_headers.get('sheets')) \
                if (int(store.get('type')) == int(FileTypeEnum.EXCEL_MERGE.value) or not is_compress) and excel_headers else '{}'
            new_model.create_time = get_now()
            new_model.is_del = False
            self.excel_result_bo.add_model(new_model)
            return True
        except:
            return False

    def _transfer_time(self, t):
        """
        数据库datetime字段 TO 字符串格式时间字段
        """
        if not t:
            return ""

        if isinstance(t, datetime.datetime):
            return d2s(t)
        elif isinstance(t, str) and t == '0000-00-00 00:00:00':
            return ""
        else:
            return t or ''

    def _office_pdf_model_to_dict(self, model, _type='info'):
        """
        office model to dict
        params model: office model object
        attrs from class define attrs
        return dict data
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.office_pdf_show_attrs:
            if not attr: continue
            if attr == 'id':
                _res[attr] = getattr(model, 'id', '')
            elif attr == 'name':
                _res[attr] = getattr(model, 'name', '')
            elif attr == 'store_name':
                _res[attr] = getattr(model, 'store_name', '')
            elif attr == 'transfer_name':
                _res[attr] = getattr(model, 'transfer_name', '')
            elif attr == 'md5_id':
                _res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'rtx_id':
                _res[attr] = getattr(model, 'rtx_id', '')
            elif attr == 'file_type':
                _res[attr] = '.pdf'
            elif attr == 'transfer':
                if _type == 'info':
                    _res[attr] = '已转换' if model.transfer else '未转换'
                else:
                    _res[attr] = True if model.transfer else False
            elif attr == 'transfer_time':
                _res[attr] = self._transfer_time(model.transfer_time)
            elif attr == 'local_url':
                _res[attr] = getattr(model, 'local_url', '')
            elif attr == 'store_url':
                _res[attr] = self.store_lib.open_download_url(store_name=model.store_url) \
                    if model.store_url else ''
            elif attr == 'transfer_url':
                _res[attr] = self.store_lib.open_download_url(store_name=model.transfer_url) \
                    if model.transfer_url else ''
            elif attr == 'mode':
                if _type == 'info':
                    _res[attr] = '通用页码' if model.mode else '指定页码'
                else:
                    _res[attr] = True if model.mode else False
            elif attr == 'start':
                _res[attr] = getattr(model, 'start', '')
            elif attr == 'end':
                _res[attr] = getattr(model, 'end', '')
            elif attr == 'pages':
                _res[attr] = getattr(model, 'pages', '')
            elif attr == 'create_time':
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'delete_rtx':
                _res[attr] = getattr(model, 'delete_rtx', '')
            elif attr == 'delete_time':
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'is_del':
                _res[attr] = True if model.is_del else False
        else:
            return _res

    def _excel_source_model_to_dict(self, model):
        """
        excel source model to dict
        params model: excel source model object
        attrs from class define attrs
        return dict data
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.excel_source_show_attrs:
            if attr == 'id':
                _res[attr] = getattr(model, 'id', '')
            elif attr == 'name':
                _res[attr] = getattr(model, 'name', '')
            elif attr == 'md5_id':
                _res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'rtx_id':
                _res[attr] = getattr(model, 'rtx_id', '')
            elif attr == 'ftypek':
                _res[attr] = getattr(model, 'ftype', '')       # ExcelSourceModel.ftype
            elif attr == 'ftypev':
                _res[attr] = getattr(model, 'enum_value', '')   # EnumModel.value.label('enum_value')
            elif attr == 'numopr':
                _res[attr] = getattr(model, 'numopr', 0)
            elif attr == 'url':
                if getattr(model, 'store_url', ''):
                    # 直接拼接的下载url，无check ping
                    _res['url'] = self.store_lib.open_download_url(store_name=model.store_url)
                    # url and check ping
                    # resp = self.store_lib.open_download(store_name=model.store_url)
                    # _res['url'] = resp.get('data').get('url') if resp.get('status_id') == 100 else ''
                else:
                    _res['url'] = ''
            elif attr == 'nsheet':
                _res['nsheet'] = getattr(model, 'nsheet', 1)    # 无值，默认为1个SHEET
            elif attr == 'set_sheet':
                """
                设置选择的sheet
                > 获取所有的sheet列表名称集合
                > 获取选择的sheet列表index索引值
                > join拼接字符串
                > 超过指定大小进行切割 + 具体查看请下载
                """
                if getattr(model, 'sheet_names', ''):
                    new_res = list()
                    set_sheet_name = list()
                    set_sheet_index = [str(i) for i in str(model.set_sheet).split(';')] if model.set_sheet else ['0']   # 默认index为0
                    for k, v in json.loads(model.sheet_names).items():
                        new_res.append({'key': k, 'value': v})
                        if str(k) in set_sheet_index:
                            set_sheet_name.append(v)
                        if int(k) >= SHEET_NUM_LIMIT:   # 加了展示条数的限制，否则页面展示太多
                            new_res.append({'key': '...N', 'value': '（具体查看请下载）'})
                            break
                    # sheet列表名称集合，[{'key': k, 'value': v}]格式
                    _res['sheet_names'] = new_res
                    set_sheet_name = ';'.join(set_sheet_name)
                    if len(set_sheet_name) > SHEET_NAME_LIMIT:  # 加了展示字数的限制，否则页面展示太多
                        set_sheet_name = '%s...具体查看请下载' % set_sheet_name[0:SHEET_NAME_LIMIT]
                    # 选择sheet列表名称，string类型（；分割）
                    _res['set_sheet_name'] = set_sheet_name
                    # 选择sheet列表index索引值集合，[]格式
                    _res['set_sheet_index'] = set_sheet_index
                else:
                    _res['sheet_names'] = []    # sheet列表名称集合，[{'key': k, 'value': v}]格式
                    _res['set_sheet_index'] = []    # 选择sheet列表index索引值集合，[]格式
                    _res['set_sheet_name'] = ''     # 选择sheet列表名称，string类型（；分割）
            elif attr == 'create_time':
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'delete_rtx':
                _res[attr] = getattr(model, 'delete_rtx', '')
            elif attr == 'delete_time':
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'is_del':
                _res[attr] = True if model.is_del else False
        else:
            return _res

    def _excel_result_model_to_dict(self, model):
        """
        excel result model to dict
        params model: excel result model object
        attrs from class define attrs
        return dict data
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.excel_result_show_attrs:
            if attr == 'id':
                _res[attr] = getattr(model, 'id', '')
            elif attr == 'name':
                _res[attr] = getattr(model, 'name', '')
            elif attr == 'md5_id':
                _res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'rtx_id':
                _res[attr] = getattr(model, 'rtx_id', '')
            elif attr == 'ftypek':
                _res[attr] = getattr(model, 'ftype', '')
            elif attr == 'ftypev':
                _res[attr] = getattr(model, 'enum_value', '')
            elif attr == 'compress':
                _res[attr] = True if model.is_compress else False
            elif attr == 'row':
                _res[attr] = getattr(model, 'row', '')
            elif attr == 'col':
                _res[attr] = getattr(model, 'col', '')
            elif attr == 'url':
                if getattr(model, 'store_url', ''):
                    # 直接拼接的下载url，无check
                    _res['url'] = self.store_lib.open_download_url(store_name=model.store_url)
                    # url and check
                    # resp = self.store_lib.open_download(store_name=model.store_url)
                    # _res['url'] = resp.get('data').get('url') if resp.get('status_id') == 100 else ''
                else:
                    _res['url'] = ''
            elif attr == 'nsheet':
                _res['nsheet'] = getattr(model, 'nsheet', 1)
            elif attr == 'nfile':
                _res['nfile'] = getattr(model, 'nfile', 1)
            elif attr == 'set_sheet':
                """
                set_sheet_name：字符串，选择的sheet名称（拼接）
                sheet_names: 列表类型，元素为{'key': k, 'value': v}格式
                set_sheet_index：列表类型，选择的sheet列表，与sheet_names搭配显示select多选
                """
                if getattr(model, 'sheet_names', ''):
                    new_res = list()
                    set_sheet_name = list()
                    for k, v in json.loads(model.sheet_names).items():
                        new_res.append({'key': k, 'value': v})
                        set_sheet_name.append(v)
                        if int(k) >= SHEET_NUM_LIMIT:
                            new_res.append({'key': '...N', 'value': '（具体查看请下载）'})
                            break
                    # sheet列表名称集合，[{'key': k, 'value': v}]格式
                    _res['sheet_names'] = new_res
                    set_sheet_name = ';'.join(set_sheet_name)
                    if len(set_sheet_name) > SHEET_NAME_LIMIT:
                        set_sheet_name = '%s...（具体查看请下载）' % set_sheet_name[0:SHEET_NAME_LIMIT]
                    # 选择sheet列表名称，string类型（；分割）
                    _res['set_sheet_name'] = set_sheet_name
                else:
                    _res['sheet_names'] = []        # sheet列表名称集合，[{'key': k, 'value': v}]格式
                    _res['set_sheet_name'] = ''     # 选择sheet列表名称，string类型（；分割）
            elif attr == 'create_time':
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'delete_rtx':
                _res[attr] = getattr(model, 'delete_rtx', '')
            elif attr == 'delete_time':
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'is_del':
                _res[attr] = True if model.is_del else False
        else:
            return _res

    def excel_source_list(self, params: dict) -> dict:
        """
        get excel source excel list by params
        params is dict
        return json data
        """
        # > no parameters
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_source_list_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # ================= parameters check and format =================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_source_list_attrs and v:   # illegal
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k or StatusMsgs.get(213), {}).json()
            if k == 'type' and int(v) not in [FileTypeEnum.EXCEL_MERGE.value, FileTypeEnum.EXCEL_SPLIT.value]:
                return Status(
                    213, 'failure', u'请求参数type值不合法', {}).json()
            if k == 'limit':
                v = int(v) if v else OFFICE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            else:
                v = str(v) if v else ''
            new_params[k] = v
        # **************** 管理员获取ALL数据 *****************
        # 权限账户
        if new_params.get('rtx_id') in auth_rtx_join([]):
            new_params.pop('rtx_id')
        # <<<<<<<<<<<<<<< models >>>>>>>>>>>>>>>>
        new_params['enum_name'] = 'excel-type'
        res, total = self.excel_source_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # format return data
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._excel_source_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def _update_file_name(self, model, new_name):
        """
        修改实际文件名称，以及store对象上的文件名称
        build in method, not allow outer to use
        get source/result file name store_name local_url store_url
        return json data

        update real file name and store file name
        """
        _res = dict()
        # check parameter
        if not model or not new_name:
            return _res
        # check model object attr
        if not model.name or not model.store_name \
                or not model.local_url or not model.store_url:
            return _res

        # 分割文件名称
        new_names = os.path.splitext(str(new_name))
        # check format
        if new_names[-1] not in self.EXCEL_FORMAT:
            new_name = '%s%s' % (new_names[0], self.DEFAULT_EXCEL_FORMAT)
        # local file name modify
        local_urls = str(model.local_url).split('/')
        new_local_url = str(model.local_url).replace(local_urls[-1], new_name)
        # check rename file exist
        if os.path.exists(new_local_url):
            new_names = os.path.splitext(str(new_name))
            new_name = '%s-%s%s' % (new_names[0], get_now(format="%Y-%m-%d-%H-%M-%S"), new_names[-1])
            new_local_url = str(model.local_url).replace(local_urls[-1], new_name)
        # modify file name
        if os.path.exists(model.local_url):
            os.rename(model.local_url, new_local_url)
        # store file rename
        try:
            store_urls = str(model.store_url).split('/')
            new_store_url = str(model.store_url).replace(store_urls[-1], new_name)
            _store_rename_res = self.store_lib.move(src_space_name=STORE_SPACE_NAME, src_store_name=model.store_name,
                                                    tar_space_name=STORE_SPACE_NAME, tar_store_name=new_store_url)
            if _store_rename_res.get('status_id') != 100:
                new_store_url = model.store_name
        except:
            new_store_url = model.store_name
        return {
            'name': new_name,
            'store_name': new_store_url,
            'local_url': new_local_url,
            'store_url': new_store_url
        }

    def excel_source_update(self, params: dict) -> dict:
        """
        update excel source file information, contain:
            - name 文件名称
            - set_sheet 设置的Sheet

        params is dict data
        return json data
        """
        # ===================== no parameters =====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_source_update_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # ===================== parameters check and format =====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_source_update_attrs and v:     # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            # parameters check
            if k == 'set_sheet':    # parameter type check
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                new_params[k] = ';'.join(v)     # 格式化成字符串存储
            elif k == 'name':   # file name check
                new_names = os.path.splitext(str(v))
                if new_names[-1] not in self.EXCEL_FORMAT:
                    return Status(
                        217, 'failure', u'文件格式只支持.xls、.xlsx', {}).json()
                if not check_length(v, 80):  # length check
                    return Status(
                        213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
                new_params[k] = str(v)
            else:
                new_params[k] = str(v)
        """       =============get model============       """
        model = self.excel_source_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 权限账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                310, 'failure', StatusMsgs.get(310), {}).json()
        """   <<<<<<<<<< update >>>>>>>>>> """
        try:
            is_update = False
            # file name to rename
            if new_params.get('name') and \
                    str(new_params.get('name')) != str(model.name):
                res = self._update_file_name(model, new_params.get('name'))
                if res:
                    model.name = res.get('name')
                    model.store_name = res.get('store_name')
                    model.local_url = res.get('local_url')
                    model.store_url = res.get('store_url')
                    is_update = True
            # file set_sheet to update
            if new_params.get('set_sheet') and \
                    str(new_params.get('set_sheet')) != str(model.set_sheet):
                model.set_sheet = new_params.get('set_sheet')
                is_update = True
            if is_update:
                self.excel_source_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def excel_source_delete(self, params: dict) -> dict:
        """
        delete one excel source excel file by params
        params is dict
        """
        # '''''''''''''''''' parameters check ''''''''''''''''
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_delete_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_delete_attrs:      # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<<     get model    >>>>>>>>>>>>>>>>
        model = self.excel_source_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 权限账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                311, 'failure', StatusMsgs.get(311), {}).json()
        try:
            # 软删除
            model.is_del = True
            model.delete_rtx = rtx_id
            model.delete_time = get_now()
            self.excel_source_bo.merge_model(model)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def excel_source_deletes(self, params: dict) -> dict:
        """
        delete many excel source excel file by params
        params is dict
        """
        # ----------- parameters check and format -----------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_deletes_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_deletes_attrs:     # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            if k == 'list':     # check type
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)
        # **************** 管理员获取ALL数据 *****************
        # 特权账号
        if new_params.get('rtx_id') in auth_rtx_join([]):
            new_params.pop('rtx_id')
        try:
            # 批量软删除
            res = self.excel_source_bo.batch_delete_by_md5(params=new_params)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()
        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def excel_merge(self, params: dict) -> dict:
        """
        operation method, many excel file to merge one excel file,
        many file list by file md5 list
        params params: request params, rtx_id and excel md5 list
        
        return json result
        """
        """ =========================== merge: 1.parameters check and format=========================== """
        # >>>>>>>> no parameters
        if not params:
            return Status(
                212, 'failure', u'缺少请求参数', {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_merge_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters format
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_merge_attrs:       # illegal parameter key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in ['blank']:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            # check: length
            if k == 'name' and not check_length(v, 80):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            # <<<<<<<<< new parameters >>>>>>>>>
            if k == 'list':     # check type
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                new_params[k] = [str(i) for i in v]     # list type
            elif k == 'blank':
                new_params[k] = int(v) if v else 0      # int type
            else:
                new_params[k] = str(v)                  # string type
        """ =========================== merge: 2.get and format data=========================== """
        # <<<<<<<<<<<< get batch merge model >>>>>>>>>>>>>>>
        res = self.excel_source_bo.get_model_by_md5_list(md5_list=new_params.get('list'))
        # no data, return
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {}).json()
        """
        格式化数据
        1.格式化指定格式
        2.判断如果包含.xls就用merge_xlrw方法，否则用merge_openpyxl
        """
        all_merge_files = list()
        # data structure: {'file': f, 'sheets': set_sheet, 'nsheet': n}
        # is_openpyxl = True
        for _r in res:
            if not _r or not _r.name or not _r.local_url: continue  # no exist -> continue
            # if os.path.splitext(str(_r.name))[-1] == '.xls':
            #     is_openpyxl = False
            all_merge_files.append({
                'file': _r.local_url,
                'sheets': str(_r.set_sheet).split(';') if _r.set_sheet else [0],
                'nsheet': int(_r.nsheet),
            })
        """ 
        =========================== merge: 3.merge=========================== 
        # many file to merge
        # extend parameter:
        #   - blank: 文件合并之间的空格数
        
        使用下列代码需要开放is_openpyxl判断
        """
        # merge_res = self.excel_lib.merge_openpyxl(new_name=new_params.get('name'), file_list=all_merge_files, blank=new_params.get('blank')) \
        #     if is_openpyxl else self.excel_lib.merge_xlrw(new_name=new_params.get('name'), file_list=all_merge_files, blank=new_params.get('blank'))

        """
        新方法：
            采取xlrd、openpyxl综合操作表格合并：
                - 读取：xlrd
                - 写入：openpyxl
            xlrd可以读取.xls、.xlsx不同格式表格数据，新版本.xlsx格式版本excel存储
        """
        merge_res = self.excel_lib.merge_new(new_name=new_params.get('name'),
                                             file_list=all_merge_files,
                                             blank=new_params.get('blank'))
        if merge_res.get('status_id') != 100:
            return Status(
                merge_res.get('status_id'), 'failure', merge_res.get('message'), {}).json()
        """ =========================== merge: 4.store and update =========================== """
        # store message to store and local db
        store_msg = {
            'name': merge_res.get('data').get('name'),
            'store_name': '%s/%s' % (get_now(format='%Y%m%d'), merge_res.get('data').get('name')),
            'path': merge_res.get('data').get('path')
        }
        # file upload to store object, manual control【上传云服务器存储】
        if OFFICE_STORE_BK:
            store_res = self.store_lib.upload(store_name=store_msg.get('store_name'),
                                              local_file=store_msg.get('path'))
            if store_res.get('status_id') != 100:
                return Status(store_res.get('status_id'),
                              'failure',
                              store_res.get('message') or StatusMsgs.get(store_res.get('status_id')),
                              {}).json()
        # file to db【本地化数据库存储】
        store_msg['rtx_id'] = new_params.get('rtx_id')
        store_msg['type'] = FileTypeEnum.EXCEL_MERGE.value
        store_msg['md5'] = md5('%s%s' % (store_msg.get('name'), get_now()))
        is_to_db = self.store_excel_result_to_db(store_msg)
        if not is_to_db:        # 本地化存储失败
            return Status(
                225, 'failure', StatusMsgs.get(225), {}).json()

        # add source file number operation 更新文件操作次数
        for _r in res:
            if not _r: continue
            try:
                _r.numopr = _r.numopr + 1
                self.excel_source_bo.merge_model(_r)
            except:
                pass

        return Status(
            100, 'success', StatusMsgs.get(100), merge_res.get('data')).json()

    def excel_history_list(self, params: dict) -> dict:
        """
        get excel history excel list from db table excel_result
        many file
        :return: json data
        """
        # ---------- ========== no params ========== -----------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_result_list_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # ************** parameters check and format **************
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_result_list_attrs and v:   # 不合法参数
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if k == 'limit':
                v = int(v) if v else OFFICE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            elif k == 'type':      # filter: check parameter type, format is [1, 2]
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s必须为list类型' % k, {}).json()
                v = [str(i) for i in v] if v else []
            elif k == 'name' and v:     # filter: like search
                v = '%' + str(v) + '%'
            elif k in ['start_time', 'end_time'] and v:   # filter: start_time, end_time
                v = d2s(v) if isinstance(v, datetime.datetime) \
                    else v
            else:
                v = str(v) if v else ''
            new_params[k] = v
        # **************** 管理员获取ALL数据 *****************
        if new_params.get('rtx_id') in auth_rtx_join([]):
            new_params.pop('rtx_id')

        """     ============ get models list ==========    """
        new_params['enum_name'] = 'excel-type'
        res, total = self.excel_result_bo.get_all(new_params)
        if not res:         # 无数据
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # format data
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._excel_result_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def excel_result_update(self, params: dict) -> dict:
        """
        update result excel file, only update file name
        params is dict
        """
        # no params
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_result_update_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # parameters check and format
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_result_update_attrs and v:     # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value check, is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            if k == 'name':     # check name and length
                new_names = os.path.splitext(str(v))
                if new_names[-1] not in self.EXCEL_FORMAT:
                    return Status(
                        217, 'failure', u'文件格式只支持.xls、.xlsx', {}).json()
                if not check_length(v, 80):  # check: length
                    return Status(
                        213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
                v = str(v)
            else:
                v = str(v)
            new_params[k] = v
        """     get model    """
        model = self.excel_result_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 权限账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                310, 'failure', StatusMsgs.get(310), {}).json()
        """ update model """
        is_update = False
        if new_params.get('name') and str(new_params.get('name')) != str(model.name):
            res = self._update_file_name(model, new_params.get('name'))
            if res:
                model.name = res.get('name')
                model.store_name = res.get('store_name')
                model.local_url = res.get('local_url')
                model.store_url = res.get('store_url')
                is_update = True
        if is_update:
            try:
                self.excel_result_bo.merge_model(model)
            except:
                return Status(
                    322, 'failure', StatusMsgs.get(322), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def excel_result_delete(self, params: dict) -> dict:
        """
        delete one excel result excel file by md5
        params is dict
        """
        # no parameters
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_delete_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # parameters check && format
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_delete_attrs:      # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>
        model = self.excel_result_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 权限账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                311, 'failure', StatusMsgs.get(311), {}).json()
        try:
            # 软删除
            model.is_del = True
            model.delete_rtx = rtx_id
            model.delete_time = get_now()
            self.excel_result_bo.merge_model(model)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def excel_result_deletes(self, params: dict) -> dict:
        """
        delete many excel result excel file by params
        params is dict
        """
        # ================= no parameters ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_deletes_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # ================= parameters check and format ====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_deletes_attrs:     # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            if k == 'list':     # type check
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)
        # **************** 管理员获取ALL数据 *****************
        # 特权账号
        if new_params.get('rtx_id') in auth_rtx_join([]):
            new_params.pop('rtx_id')
        try:
            # 批量软删除
            res = self.excel_result_bo.batch_delete_by_md5(params=new_params)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()

        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list')) - res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list')) - res)}).json()

    def excel_init_split_params(self, params: dict) -> dict:
        """
        initialize the result excel file split parameter
        params is dict
        return json data, data contain:
            - sheet_index
            - sheet_names
            - column_names
            - excel_split_store
            - split_type
            - bool_type
        """
        # ------------- parameters check and format ---------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_init_split_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # >>>>>>>>>>>> new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_init_split_attrs:      # 不合法的参数key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value不允许为空
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>>>>
        model = self.excel_source_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 权限账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        """ ------ 格式化数据 ------ """
        # data info
        sheet_names = list()
        sheet_index = str(model.set_sheet) if model.set_sheet else '0'
        if model.sheet_names:
            for k, v in json.loads(model.sheet_names).items():
                sheet_names.append({'label': str(v), 'value': str(k)})
        column_names = list()
        # 添加默认ID
        column_names.append({'label': '序号自增', 'value': '9999'})
        sheet_columns_json = json.loads(model.sheet_columns)
        if sheet_columns_json and sheet_columns_json.get(str(sheet_index)):
            for item in sheet_columns_json.get(str(sheet_index)):
                column_names.append({'label': str(item.get('value')) if item.get('value') else '/', 'value': str(item.get('key'))})
        # enum info
        names = ['excel-split-store', 'excel-num', 'bool-type']
        enums_models = self.enum_bo.get_model_by_names(names)
        template_list = list()
        for e in enums_models:
            template_list.append({'name': str(e.name), 'label': str(e.value), 'value': str(e.key)})
        enums_models_dict = dict()
        template_list.sort(key=itemgetter('name'))
        for key, group in groupby(template_list, key=itemgetter('name')):
            enums_models_dict[key] = list(group)
        data = {
            'sheet_index': sheet_index,
            'sheet_names': sheet_names,
            'column_names': column_names,
            'excel_split_store': enums_models_dict.get('excel-split-store'),
            'split_type': enums_models_dict.get('excel-num'),
            'bool_type': enums_models_dict.get('bool-type')
        }
        return Status(
            100, 'success', StatusMsgs.get(100), data
        ).json()

    def excel_sheet_header(self, params: dict) -> dict:
        """
        get sheet headers by sheet index from excel_source table
        params is dict
        """
        # ------------ parameters check and format --------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_sheet_header_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_sheet_header_attrs:    # 不合法key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            v = str(v)
            if not v:       # check value is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = v
        # <<<<<<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>>>>
        model = self.excel_source_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 权限账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        # format return data
        headers = list()
        headers.append({'label': '序号自增', 'value': '9999'})
        sheet_columns_json = json.loads(model.sheet_columns)
        if sheet_columns_json and sheet_columns_json.get(str(new_params.get('sheet'))):
            for k, v in enumerate(sheet_columns_json.get(str(new_params.get('sheet')))):
                headers.append({'label': str(v) if v else '/', 'value': str(k)})
        data = {
            'headers': headers,
            'md5': new_params.get('md5')
        }
        return Status(
            100, 'success', StatusMsgs.get(100), data
        ).json()

    def excel_split(self, params):
        """
        split method, split parameters is many
        function: one file to split many file
        one excel file to split many file
        """
        # ******************* no parameters *******************
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_split_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        """ 参数check """
        # ====================== init enums info ======================
        names = ['excel-split-store', 'excel-num', 'bool-type']
        excel_split_store = list()
        excel_num = list()
        bool_type = list()
        enums_models = self.enum_bo.get_model_by_names(names)
        if enums_models:
            for e in enums_models:
                if e.name == 'bool-type':
                    bool_type.append(str(e.key))
                elif e.name == 'excel-split-store':
                    excel_split_store.append(str(e.key))
                elif e.name == 'excel-num':
                    excel_num.append(str(e.key))
        excel_split_store = excel_split_store \
            if excel_split_store else EXCEL_SPLIT_STORE
        excel_num = excel_num \
            if excel_num else EXCEL_NUM
        bool_type = bool_type \
            if bool_type else BOOL
        # ====================== parameters common check ======================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_split_attrs:       # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if k == 'columns':      # columns字段列检查
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}).json()
            if k != 'name' and not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            if k == 'store' and v not in excel_split_store:
                return Status(
                    213, 'failure', u'请求参数%s值不合法' % k, {}).json()
            elif k == 'split' and v not in excel_num:
                return Status(
                    213, 'failure', u'请求参数%s值不合法' % k, {}).json()
            elif k == 'header' and v not in bool_type:
                return Status(
                    213, 'failure', u'请求参数%s值不合法' % k, {}).json()

            new_params[k] = str(v) if k != 'columns' else v
        if not new_params.get('sheet'):
            new_params['sheet'] = '0'
        # ---------------------- check params ok...... -----------------------

        # <<<<<<<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>>>>>>
        model = self.excel_source_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 权限账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        # file not exist
        if not model.local_url or \
                not os.path.exists(model.local_url):
            return Status(
                226, 'failure', StatusMsgs.get(226), {}).json()
        """ =================== split ===================="""
        # 无新文件名称，以原始文件为名称
        if not new_params.get('name'):
            name = model.name
            # default is 1 多表一Sheet(压缩) 2 一表多Sheet(不压缩)
            store = str(new_params.get('store'))
            if store == '1':
                if os.path.splitext(name)[-1] in self.EXCEL_FORMAT:
                    name = os.path.splitext(name)[0]
            new_params['name'] = name
        # 无sheet，默认index为0
        sheet = new_params.get('sheet') or '0'
        headers = model.headers
        # 分割表行数检查
        row = 0
        if headers:  # db get row
            sheet_header = json.loads(headers).get(str(sheet))
            if sheet_header:
                row = sheet_header.get('row') or 0
        if row == 0:   # file get row
            sheets = self.excel_lib.read_headers(model.local_url).get('sheets')
            if sheets:
                sheet_header = sheets.get(int(sheet))
                if sheet_header:
                    row = sheet_header.get('row')
        if row == 0:        # 0行无数据
            return Status(
                227, 'failure', StatusMsgs.get(227), {}).json()
        if row >= 65535:        # 最大行数65535
            return Status(
                228, 'failure', StatusMsgs.get(228), {}).json()
        # =========================== main method ===========================
        try:
            resp_json = self.excel_lib.split_xlrw(file=model.local_url,
                                                  name=new_params.get('name'),
                                                  sheet=new_params.get('sheet'),
                                                  type=new_params.get('split'),
                                                  store=new_params.get('store'),
                                                  rule=new_params.get('columns'),
                                                  title=new_params.get('header'))
        except Exception as e:
            # 异常处理
            print('ExcelLib split excel error: %s' % e)
            return Status(
                307, 'failure', 'Excel处理split失败', {}
            ).json()

        # ---------------- split failure ----------------
        if resp_json.get('status_id') != 100:
            return Status(
                307, 'failure', resp_json.get('message'), {}).json()
        # ---------------- split success ----------------
        data = resp_json.get('data')
        # file upload to store object, manual control【存储云服务器】
        store_name = '%s/%s' % (get_now('%Y%m%d'), data.get('name'))
        if OFFICE_STORE_BK:
            store_res = self.store_lib.upload(store_name=store_name, local_file=data.get('path'))
            if store_res.get('status_id') != 100:
                return Status(store_res.get('status_id'),
                              'failure',
                              store_res.get('message') or StatusMsgs.get(store_res.get('status_id')),
                              {}).json()
        # file to db【存储到数据库】
        new_data = {
            'name': data.get('name'),
            'rtx_id': new_params.get('rtx_id'),
            'store_name': store_name,
            'type': FileTypeEnum.EXCEL_SPLIT.value,
            'md5': md5('%s%s' % (data.get('name'), get_now())),
            'path': data.get('path'),
            'compress': data.get('compress') or False,
            'nfile': data.get('nfile') or 1
        }
        is_to_db = self.store_excel_result_to_db(new_data)
        if not is_to_db:
            return Status(
                225, 'failure', StatusMsgs.get(225), {}).json()

        # update excel result number operation
        model.numopr = model.numopr + 1
        self.excel_result_bo.merge_model(model)

        return Status(
            100, 'success', StatusMsgs.get(100), {}
        ).json()

    def pdf2word_list(self, params: dict) -> dict:
        """
        get pdf2word file list by params
        params is dict
        return json data
        """
        # >>>>>>>>>> no parameters <<<<<<<<<<<
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_pdf2word_list_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # ================= parameters check and format =================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_pdf2word_list_attrs and v:     # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if k == 'type' and int(v) != FileTypeEnum.PDF.value:    # value is not null
                return Status(
                    213, 'failure', u'请求参数type值不合法', {}).json()
            if k == 'limit':
                v = int(v) if v else OFFICE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            else:
                v = str(v) if v else ''
            new_params[k] = v
        # **************** 管理员获取ALL数据 *****************
        # 特权账号
        if new_params.get('rtx_id') in auth_rtx_join([]):
            new_params.pop('rtx_id')
        # <<<<<<<<<<<<<< get all models >>>>>>>>>>>>>>>
        res, total = self.office_pdf_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # format return data
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._office_pdf_model_to_dict(_d, _type='info')
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def office_pdf_detail(self, params):
        """
        get office pdf file detail information by file md5
        :return: json data
        """
        # =================== parameters check and format ===================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_detail_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_detail_attrs:      # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # =================== parameters ok.......... ===================
        # <<<<<<<<<<< get model >>>>>>>>>>>>
        model = self.office_pdf_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                302, 'failure', '数据已删除' or StatusMsgs.get(302), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 权限账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        # return
        return Status(
            100, 'success', StatusMsgs.get(100), self._office_pdf_model_to_dict(model, _type='detail')
        ).json()

    def office_pdf_update(self, params):
        """
        update office pdf file information, contain:
            - name 文件名称
            - start 转换开始页
            - end 转换结束页
            - pages 指定转换页列表
            - mode 模式
        by file md5
        :return: json data
        """
        # --------------- no parameters ---------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_pdf_update_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # --------------- parameters check and format ---------------
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_pdf_update_attrs and v:        # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if k == 'mode':  # parameter pages
                if not isinstance(v, bool):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是Boolean' % k, {}).json()
                new_params[k] = v
            elif k in ['start', 'end']:     # special check
                if v:
                    try:
                        v_int = int(v)
                    except:
                        return Status(
                            213, 'failure', u'请求参数%s类型必须是整数' % k, {}).json()
                    if v_int > 10000:
                        return Status(
                            213, 'failure', u'请求参数%s最大限制10000' % k, {}).json()
                    if v_int < 1:
                        return Status(
                            213, 'failure', u'请求参数%s最小值为1' % k, {}).json()
                    new_params[k] = v_int
                else:
                    new_params[k] = ''
            elif k == 'pages':      # check special parameter
                if v:
                    v_s = str(v).strip().split(',')     # 去空格在分割
                    if len(v_s) <= 0:    # 无可用分页数据，直接continue
                        new_params[k] = ''
                        continue
                    for _v in v_s:
                        if not _v: continue
                        if not str(_v).isdigit():
                            return Status(
                                213, 'failure', u'请检查指定分页数据，用英文,分割', {}).json()
                    if not check_length(v, 120):
                        return Status(
                            213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
                    new_params[k] = str(v)
                else:
                    new_params[k] = ''
            else:
                new_params[k] = str(v)
        if new_params.get('start') and new_params.get('end'):
            if new_params.get('start') > new_params.get('end'):
                return Status(
                    213, 'failure', u'起始页码不得大于结束页码', {}).json()
        # ================= check ok......... =================
        # <<<<<<<< get model >>>>>>>>>>
        model = self.office_pdf_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 特权账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                310, 'failure', StatusMsgs.get(310), {}).json()

        try:
            # update
            model.start = new_params.get('start')
            model.end = new_params.get('end')
            model.pages = new_params.get('pages')
            model.mode = new_params.get('mode')
            self.excel_source_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def office_pdf_delete(self, params: dict) -> dict:
        """
        delete one office pdf file by md5
        :return: json data
        """
        # ================ check parameters ================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_delete_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters format
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_delete_attrs:      # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)
        # # # # # # # # get model # # # # # # # #
        model = self.office_pdf_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 权限账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                311, 'failure', StatusMsgs.get(311), {}).json()
        try:
            # 软删除
            model.is_del = True
            model.delete_rtx = rtx_id
            model.delete_time = get_now()
            self.office_pdf_bo.merge_model(model)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def office_pdf_deletes(self, params):
        """
        delete many office pdf file by md5 list
        :return: json data
        """
        # ------------------ check parameters -----------------
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_deletes_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters format
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_deletes_attrs:     # illegal key
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # value is not null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            if k == 'list':  # type check
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)
        # **************** 管理员获取ALL数据 *****************
        # 特权账号
        if new_params.get('rtx_id') in auth_rtx_join([]):
            new_params.pop('rtx_id')
        try:
            # 批量软删除
            res = self.office_pdf_bo.batch_delete_by_md5(params=new_params)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()

        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list')) - res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list')) - res)}).json()

    def office_pdf_to(self, params):
        """
        office pdf file convert to word file, one file to convert:
            1.check current file set data
            2.convert pdf file to word
            3.convert success to store object
            4.update transfer information
        save office pdf file information, contain:
            - name 文件名称
            - start 转换开始页
            - end 转换结束页
            - pages 指定转换页列表
            - mode 模式
        by file md5
        :return: json data
        """
        # no parameters
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_pdf_convert_need_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        """ ************************************* check parameters ***************************************** """
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_pdf_convert_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # parameters check
            if k == 'mode':  # parameter pages
                if not isinstance(v, bool):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是Boolean' % k, {}).json()
                new_params[k] = v
            elif k in ['start', 'end']:  # check integer
                if v:
                    try:
                        v_int = int(v)
                    except:
                        return Status(
                            213, 'failure', u'请求参数%s类型必须是整数' % k, {}).json()
                    if v_int > 10000:
                        return Status(
                            213, 'failure', u'请求参数%s最大限制10000' % k, {}).json()
                    if v_int < 1:
                        return Status(
                            213, 'failure', u'请求参数%s最小值为1' % k, {}).json()
                    new_params[k] = v_int
                else:
                    new_params[k] = ''
            elif k == 'pages':  # check special parameter
                if v:
                    v_s = str(v).strip().split(',')  # 去空格在分割
                    if len(v_s) <= 0:  # 无可用分页数据，直接continue
                        new_params[k] = ''
                        continue
                    for _v in v_s:
                        if not _v: continue
                        if not str(_v).isdigit():
                            return Status(
                                213, 'failure', u'请检查指定分页数据，用英文,分割', {}).json()
                    if not check_length(v, 120):
                        return Status(
                            213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
                    new_params[k] = str(v)
                else:
                    new_params[k] = ''
            else:
                new_params[k] = str(v)
        if new_params.get('start') and new_params.get('end'):
            if new_params.get('start') > new_params.get('end'):
                return Status(
                    213, 'failure', u'起始页码不得大于结束页码', {}).json()
        """ ************************************* convert: 1.check data ***************************************** """
        model = self.office_pdf_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 权限账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()

        """ ************************************* convert: 2.convert ***************************************** """
        # 初始化数据
        _pdf_files = dict()
        """
        pdf_list data structure:
        {
            md5: {
                pdf: pdf file,
                word: word name,
                start: start page,
                end: end page,
                pages: page list
            },
            md5: {
                pdf: pdf file,
                word: word name,
                start: start page,
                end: end page,
                pages: page list
            }
            ...
        }
        """
        _d = {'pdf': model.local_url, 'word': new_params.get('name'), 'start': '', 'end': '', 'pages': []}
        if model.mode:      # 通用页码模式
            _d['start'] = model.start
            _d['end'] = model.end
        else:       # 指定页码模式
            _d['pages'] = model.pages.split(',') if model.pages else []

        _pdf_files[model.md5_id] = _d
        _to_res = self.file_lib.pdf2word(pdf_list=_pdf_files, is_multi_processing=False)
        _status_id = _to_res.get('status_id')
        if _status_id != 100 or not _to_res.get('data') \
                or not _to_res.get('data').get(model.md5_id) \
                or not _to_res.get('data').get(model.md5_id).get('ok'):
            return Status(
                470, 'failure', '文件PDF转WORD失败' or StatusMsgs.get(470), {}).json()
        """ ************************************* convert: 3.store file ***************************************** """
        transfer_name = _to_res.get('data').get(model.md5_id).get('name')
        word_file = _to_res.get('data').get(model.md5_id).get('word')
        if not transfer_name or not word_file \
                or not os.path.exists(word_file) or not os.path.isfile(word_file):
            return Status(
                470, 'failure', '文件PDF转WORD失败' or StatusMsgs.get(470), {}).json()
        transfer_store_name = '%s/%s' % (get_now(format="%Y%m%d"), transfer_name)
        store_res = self.store_lib.upload(store_name=transfer_store_name, local_file=word_file)
        if store_res.get('status_id') != 100:
            return Status(
                store_res.get('status_id'), 'failure',
                store_res.get('message') or StatusMsgs.get(store_res.get('status_id')),
                {}).json()
        """ ************************************* convert: 4.update transfer ***************************************** """
        # update data
        try:
            model.start = new_params.get('start')
            model.end = new_params.get('end')
            model.pages = new_params.get('pages')
            model.mode = new_params.get('mode')
            model.transfer = True
            model.transfer_name = transfer_store_name
            model.transfer_time = get_now()
            model.transfer_url = transfer_store_name
            self.excel_source_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}).json()

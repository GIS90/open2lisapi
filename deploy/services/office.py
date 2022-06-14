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
from deploy.utils.file_lib import FileLib
from deploy.utils.store_lib import StoreLib
from deploy.utils.excel_lib import ExcelLib
from deploy.bo.excel_source import ExcelSourceBo
from deploy.bo.excel_result import ExcelResultBo
from deploy.bo.enum import EnumBo
from deploy.bo.office import OfficeBo

from deploy.config import STORE_BASE_URL, STORE_SPACE_NAME, \
    EXCEL_LIMIT, EXCEL_STORE_BK, \
    ADMIN, SHEET_NAME_LIMIT, SHEET_NUM_LIMIT
from deploy.utils.utils import get_now, d2s, md5, s2d, check_length
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
        'set_sheet',  # sheet_names Sheet名称列表（key value格式）
                      # set_sheet_index 选择的Sheet索引，List类型
                      # set_sheet_name 选择的Sheet名称，string类型（；分割）
        # 'sheet_columns',
        'create_time'
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
        'create_time'
    ]

    EXCEL_FORMAT = ['.xls', '.xlsx']

    DEFAULT_EXCEL_FORMAT = '.xlsx'

    def __init__(self):
        """
        excel service class initialize
        """
        super(OfficeService, self).__init__()
        self.excel_lib = ExcelLib()
        self.file_lib = FileLib()
        self.store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)
        self.excel_source_bo = ExcelSourceBo()
        self.excel_result_bo = ExcelResultBo()
        self.enum_bo = EnumBo()
        self.office_bo = OfficeBo()

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

    def store_office_to_db(self, store):
        """
        store office file message to db
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
            new_model = self.office_bo.new_mode()
            new_model.rtx_id = store.get('rtx_id')
            new_model.name = store.get('name')
            new_model.store_name = store.get('store_name')
            new_model.md5_id = store.get('md5')
            new_model.file_type = store.get('file_type')
            new_model.transfer = False
            new_model.local_url = store.get('path')
            new_model.store_url = store.get('store_name')
            new_model.create_time = get_now()
            new_model.is_del = False
            self.office_bo.add_model(new_model)
            return True
        except:
            return False

    def store_excel_source_to_db(self, store):
        """
        store excel source file message to db
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
            # 获取文件header
            excel_headers = self.get_excel_headers(store.get('path'))
            # create new mode
            new_model = self.excel_source_bo.new_mode()
            new_model.rtx_id = store.get('rtx_id')
            new_model.name = store.get('name')
            new_model.store_name = store.get('store_name')
            new_model.md5_id = store.get('md5')
            new_model.ftype = store.get('excel_sub_type')
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

        try:
            is_compress = store.get('compress') or False
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
            new_model.row = excel_headers.get('sheets')[0].get('row') \
                if (int(store.get('type')) == int(EXCEL_MERGE) or not is_compress) and excel_headers else 0
            new_model.col = excel_headers.get('sheets')[0].get('col') \
                if (int(store.get('type')) == int(EXCEL_MERGE) or not is_compress) and excel_headers else 0
            new_model.nsheet = excel_headers.get('nsheet') \
                if (int(store.get('type')) == int(EXCEL_MERGE) or not is_compress) and excel_headers else 0
            new_model.sheet_names = json.dumps(excel_headers.get('names')) \
                if (int(store.get('type')) == int(EXCEL_MERGE) or not is_compress) and excel_headers else '{}'
            new_model.sheet_columns = json.dumps(excel_headers.get('columns')) \
                if (int(store.get('type')) == int(EXCEL_MERGE) or not is_compress) and excel_headers else '{}'
            new_model.headers = json.dumps(excel_headers.get('sheets')) \
                if (int(store.get('type')) == int(EXCEL_MERGE) or not is_compress) and excel_headers else '{}'
            new_model.create_time = get_now()
            new_model.is_del = False
            self.excel_result_bo.add_model(new_model)
            return True
        except:
            return False

    def _source_model_to_dict(self, model):
        """
        excel source model to dict
        params model: source model object
        attrs from class define attrs
        return dict data
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.excel_source_show_attrs:
            if attr == 'id':
                _res[attr] = model.id
            elif attr == 'name':
                _res[attr] = model.name
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id
            elif attr == 'ftypek':
                _res[attr] = model.ftype
            elif attr == 'ftypev':
                _res[attr] = model.value
            elif attr == 'numopr':
                _res[attr] = model.numopr or 0
            elif attr == 'url':
                if model.store_url:
                    # 直接拼接的下载url，无check ping
                    _res['url'] = self.store_lib.open_download_url(store_name=model.store_url)
                    # url and check ping
                    # resp = self.store_lib.open_download(store_name=model.store_url)
                    # _res['url'] = resp.get('data').get('url') if resp.get('status_id') == 100 else ''
                else:
                    _res['url'] = ''
            elif attr == 'nsheet':
                _res['nsheet'] = model.nsheet if model.nsheet else 1    # 无值，默认为1个SHEET
            elif attr == 'set_sheet':
                if model.sheet_names:
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
            elif attr == 'create_time':
                _res['create_time'] = d2s(model.create_time) if model.create_time else ''
        else:
            return _res

    def _result_model_to_dict(self, model):
        """
        excel result model to dict
        params model: result model object
        attrs from class define attrs
        return dict data
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.excel_result_show_attrs:
            if attr == 'id':
                _res[attr] = model.id
            elif attr == 'name':
                _res[attr] = model.name
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id
            elif attr == 'ftypek':
                _res[attr] = model.ftype
            elif attr == 'ftypev':
                _res[attr] = model.value
            elif attr == 'compress':
                _res[attr] = True if model.is_compress else False
            elif attr == 'row':
                _res[attr] = model.row if model.row else ''
            elif attr == 'col':
                _res[attr] = model.col if model.col else ''
            elif attr == 'url':
                if model.store_url:
                    # 直接拼接的下载url，无check
                    _res['url'] = self.store_lib.open_download_url(store_name=model.store_url)
                    # url and check
                    # resp = self.store_lib.open_download(store_name=model.store_url)
                    # _res['url'] = resp.get('data').get('url') if resp.get('status_id') == 100 else ''
                else:
                    _res['url'] = ''
            elif attr == 'nsheet':
                _res['nsheet'] = model.nsheet if model.nsheet else 1
            elif attr == 'nfile':
                _res['nfile'] = model.nfile if model.nfile else 1
            elif attr == 'set_sheet':
                if model.sheet_names:
                    new_res = list()
                    set_sheet_name = list()
                    for k, v in json.loads(model.sheet_names).items():
                        new_res.append({'key': k, 'value': v})
                        set_sheet_name.append(v)
                        if int(k) >= SHEET_NUM_LIMIT:
                            new_res.append({'key': '...N', 'value': '（具体查看请下载）'})
                            break
                    _res['sheet_names'] = new_res
                    set_sheet_name = ';'.join(set_sheet_name)
                    if len(set_sheet_name) > SHEET_NAME_LIMIT:
                        set_sheet_name = '%s...（具体查看请下载）' % set_sheet_name[0:SHEET_NAME_LIMIT]
                    _res['set_sheet_name'] = set_sheet_name
                else:
                    _res['sheet_names'] = []
                    _res['set_sheet_name'] = ''
            elif attr == 'create_time':
                _res['create_time'] = d2s(model.create_time) if model.create_time else ''
        else:
            return _res

    def excel_source_list(self, params):
        """
        get excel source excel list by params
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
            if k not in self.req_source_list_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if k == 'type' and int(v) not in [int(EXCEL_MERGE), int(EXCEL_SPLIT)]:
                return Status(
                    213, 'failure', u'请求参数type值不合法', {}
                ).json()
            if k == 'limit':
                v = int(v) if v else EXCEL_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            else:
                v = str(v) if v else ''
            new_params[k] = v
        new_params['enum_name'] = 'excel-type'
        res, total = self.excel_source_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}
            ).json()

        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._source_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def office_upload(self, params, upload_file, is_check_fmt: bool = True):
        """
        one office file upload to server(file store object)
        params params: request params, rtx_id and excel type
        params upload_file: excel upload file
        params is_check_fmt: file is or not check format
        params is_store_bk: file is or not upload to store server 对象存储备份

        excel upload to qiniu store server
        1.local store
        2.upload to qiniu store server

        return json data
        """
        # no parameters, return
        if not params:
            return Status(
                212, 'failure', u'缺少请求参数' or StatusMsgs.get(212), {}).json()

        for k, v in params.items():
            if not k: continue
            # illegal parameters check
            if k not in self.req_upload_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            # value check
            if not v and k in ['rtx_id', 'file_type']:
                return Status(
                    212, 'failure', u'未指定%s请求参数' % k, {}
                ).json()
        # excel parameters check
        if int(params.get('file_type')) == 2 and \
                int(params.get('excel_sub_type')) not in [EXCEL_MERGE, EXCEL_SPLIT]:
            return Status(
                213, 'failure', u'请求参数excel_sub_type值不合法', {}
            ).json()

        f_name = upload_file.filename   # file object
        # file format filter
        if is_check_fmt and not self.file_lib.allow_format_fmt(f_name):
            return Status(
                217, 'failure', StatusMsgs.get(217), {}).json()
        # file local store
        is_ok, store_msg = self.file_lib.store_file(
            upload_file, compress=False, is_md5_store_name=False)
        if not is_ok:
            return Status(
                220, 'failure', StatusMsgs.get(220), {}).json()
        # file upload to store object, manual control
        if EXCEL_STORE_BK:
            store_res = self.store_lib.upload(store_name=store_msg.get('store_name'),
                                              local_file=store_msg.get('path'))
            if store_res.get('status_id') != 100:
                return Status(store_res.get('status_id'),
                              'failure',
                              store_res.get('message') or StatusMsgs.get(store_res.get('status_id')),
                              {}).json()

        # file to db
        store_msg['rtx_id'] = params.get('rtx_id')
        store_msg['file_type'] = params.get('file_type')
        store_msg['excel_sub_type'] = params.get('excel_sub_type')
        # 存储文件记录到数据库，依据file_type进行不同存储
        file_type = int(params.get('file_type'))
        if file_type == FileTypeEnum.WORD.value:   # word
            pass
        elif file_type == FileTypeEnum.EXCEL.value:   # excel
            is_to_db = self.store_excel_source_to_db(store_msg)
        elif file_type == FileTypeEnum.PPT.value:   # ppt
            pass
        elif file_type == FileTypeEnum.TEXT.value:   # text
            pass
        elif file_type == FileTypeEnum.PDF.value:   # pdf
            is_to_db = self.store_office_to_db(store_msg)
        else:   # other
            pass
        if not is_to_db:
            return Status(
                225, 'failure', StatusMsgs.get(225), {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {}).json()

    def office_upload_m(self, params, upload_files, is_check_fmt: bool = True):
        """
        多文件上传 && 存储（many office file to upload and store）
        params params: request params
        params upload_files: excel upload file
        params is_check_fmt: file is or not check format

        excel upload to qiniu store server
        1.local store
        2.upload to qiniu store server
        """
        if not params:
            return Status(
                212, 'failure', u'缺少请求参数', {}).json()

        success_list = list()
        failure_list = list()
        # TODO 循环的方式进行存储文件，后期改成多进程
        for uf in upload_files:
            try:
                if not uf: continue
                store_res = self.office_upload(params=params, upload_file=upload_files.get(uf))
                store_res_json = json.loads(store_res)
                success_list.append(uf) if store_res_json.get('status_id') == 100 \
                    else failure_list.append(uf)
            except:
                failure_list.append(uf)
        if upload_files and len(failure_list) == len(upload_files):
            return Status(
                223, 'failure', '文件上传失败' or StatusMsgs.get(223), {}).json()
        if failure_list:
            return Status(
                224, 'failure', u'文件上传：成功[%s]，失败[%s]' % (len(success_list), len(failure_list)),
                {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {}).json()

    def _update_file_name(self, model, new_name):
        """
        build in method, not allow outer to use
        get source/result file name store_name local_url store_url
        return json data

        update real file name and store file name
        """
        _res = dict()
        # check
        if not model or not new_name:
            return _res
        if not model.name or not model.store_name \
                or not model.local_url or not model.store_url:
            return _res

        new_names = os.path.splitext(str(new_name))
        # check format
        if new_names[-1] not in self.EXCEL_FORMAT:
            new_name = '%s%s' % (new_names[0], self.DEFAULT_EXCEL_FORMAT)
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

    def excel_source_update(self, params):
        """
        update excel source file information, contain:
            - name 文件名称
            - set_sheet 设置的Sheet

        params is dict data
        return json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_source_update_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}
                ).json()
            # parameters check
            if k == 'set_sheet':    # parameter type check
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                new_params[k] = ';'.join(v) # 格式化成字符串存储
            elif k == 'name':   # file name check
                new_names = os.path.splitext(str(v))
                if new_names[-1] not in self.EXCEL_FORMAT:
                    return Status(
                        217, 'failure', u'文件格式只支持.xls、.xlsx', {}
                    ).json()
                if not check_length(v, 80):  # length check
                    return Status(
                        213, 'failure', u'请求参数%s长度超限制' % k, {}
                    ).json()
                new_params[k] = str(v)
            else:
                new_params[k] = str(v)

        model = self.excel_source_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}
            ).json()
        # deleted
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}
            ).json()
        # authority
        rtx_id = new_params.get('rtx_id')
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                310, 'failure', StatusMsgs.get(310), {}
            ).json()

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
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def excel_source_delete(self, params):
        """
        delete one excel source excel file by params
        params is dict
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_delete_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            new_params[k] = str(v)

        model = self.excel_source_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}
            ).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}
            ).json()
        # authority
        rtx_id = new_params.get('rtx_id')
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                311, 'failure', StatusMsgs.get(311), {}
            ).json()
        model.is_del = True
        model.delete_rtx = rtx_id
        model.delete_time = get_now()
        self.excel_source_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def excel_source_deletes(self, params):
        """
        delete many excel source excel file by params
        params is dict
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_deletes_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v: # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            if k == 'list': # check type
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)

        res = self.excel_source_bo.batch_delete_by_md5(params=new_params)
        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "删除结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def excel_merge(self, params):
        """
        many excel file to merge one excel file,
        many file list by file md5 list
        params params: request params, rtx_id and excel md5 list
        
        return json result
        """
        if not params:
            return Status(
                212, 'failure', u'缺少请求参数', {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_merge_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            # check: value is not null
            if not v and k != 'blank':
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            # check: length
            if k == 'name' and not check_length(v, 80):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}
                ).json()

            if k == 'list':     # check type
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                new_params[k] = [str(i) for i in v]
            elif k == 'blank':
                new_params[k] = int(v) if v else 0
            else:
                new_params[k] = str(v)

        res = self.excel_source_bo.get_model_by_md5_list(md5_list=new_params.get('list'))
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {}
            ).json()
        all_merge_files = list()
        # data structure: {'file': f, 'sheets': set_sheet, 'nsheet': n}
        is_openpyxl = True
        for _r in res:
            if not _r or not _r.name or not _r.local_url: continue
            if os.path.splitext(str(_r.name))[-1] == '.xls':
                is_openpyxl = False
            all_merge_files.append({
                'file': _r.local_url,
                'sheets': str(_r.set_sheet).split(';') if _r.set_sheet else [0],
                'nsheet': int(_r.nsheet),
            })
        # many file to merge
        # extend parameter:
        #   - blank: 文件合并之间的空格数
        merge_res = self.excel_lib.merge_openpyxl(new_name=new_params.get('name'), file_list=all_merge_files, blank=new_params.get('blank')) \
            if is_openpyxl else self.excel_lib.merge_xlrw(new_name=new_params.get('name'), file_list=all_merge_files, blank=new_params.get('blank'))
        if merge_res.get('status_id') != 100:
            return Status(
                merge_res.get('status_id'), 'failure', merge_res.get('message'), {}
            ).json()
        store_msg = {
            'name': merge_res.get('data').get('name'),
            'store_name': '%s/%s' % (get_now(format='%Y%m%d'), merge_res.get('data').get('name')),
            'path': merge_res.get('data').get('path')
        }
        # file upload to store object, manual control
        if EXCEL_STORE_BK:
            store_res = self.store_lib.upload(store_name=store_msg.get('store_name'),
                                              local_file=store_msg.get('path'))
            if store_res.get('status_id') != 100:
                return Status(store_res.get('status_id'),
                              'failure',
                              store_res.get('message') or StatusMsgs.get(store_res.get('status_id')),
                              {}).json()
        # file to db
        store_msg['rtx_id'] = new_params.get('rtx_id')
        store_msg['type'] = EXCEL_MERGE
        store_msg['md5'] = md5(store_msg.get('name'))
        is_to_db = self.store_excel_result_to_db(store_msg)
        if not is_to_db:
            return Status(
                225, 'failure', StatusMsgs.get(225), {}).json()

        # add source file number operation
        for _r in res:
            if not _r: continue
            _r.numopr = _r.numopr + 1
            self.excel_source_bo.merge_model(_r)

        return Status(
            100, 'success', StatusMsgs.get(100), merge_res.get('data')
        ).json()

    def excel_history_list(self, params):
        """
        get result excel list by params
        params is dict

        return json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        # parameters check
        for k, v in params.items():
            if not k: continue
            if k not in self.req_result_list_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if k == 'limit':
                v = int(v) if v else EXCEL_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            elif k == 'type':      # filter: check parameter type, format is [1, 2]
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s必须为list类型' % k, {}
                    ).json()
                v = [str(i) for i in v] if v else []
            elif k == 'name' and v:     # filter: like search
                v = '%' + str(v) + '%'
            elif k == 'start_time' and v:   # filter: start_time
                v = d2s(v) if isinstance(v, datetime.datetime) \
                    else '%s 00:00:00' % v
            elif k == 'end_time' and v:   # filter: end_time
                v = d2s(v) if isinstance(v, datetime.datetime) \
                    else '%s 23:59:59' % v
            else:
                v = str(v) if v else ''
            new_params[k] = v
        new_params['enum_name'] = 'excel-type'
        res, total = self.excel_result_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}
            ).json()

        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._result_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def excel_result_update(self, params):
        """
        update result excel file, only update file name
        params is dict
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_result_update_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v:       # value check, is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}
                ).json()
            if k == 'name':     # check name and length
                new_names = os.path.splitext(str(v))
                if new_names[-1] not in self.EXCEL_FORMAT:
                    return Status(
                        217, 'failure', u'文件格式只支持.xls、.xlsx', {}
                    ).json()
                if not check_length(v, 80):  # check: length
                    return Status(
                        213, 'failure', u'请求参数%s长度超限制' % k, {}
                    ).json()
                v = str(v)
            else:
                v = str(v)
            new_params[k] = v

        model = self.excel_result_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}
            ).json()
        # deleted
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}
            ).json()
        # authority
        rtx_id = new_params.get('rtx_id')
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                310, 'failure', StatusMsgs.get(310), {}
            ).json()

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
            self.excel_result_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def excel_result_delete(self, params):
        """
        delete one result excel file by params
        params is dict
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        # parameters check
        for k, v in params.items():
            if not k: continue
            if k not in self.req_delete_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            new_params[k] = str(v)

        model = self.excel_result_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}
            ).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}
            ).json()
        # authority
        rtx_id = new_params.get('rtx_id')
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                311, 'failure', StatusMsgs.get(311), {}
            ).json()
        model.is_del = True
        model.delete_rtx = rtx_id
        model.delete_time = get_now()
        self.excel_result_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def excel_result_deletes(self, params):
        """
        delete many excel result excel file by params
        params is dict
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        # parameters check
        for k, v in params.items():
            if not k: continue
            if k not in self.req_deletes_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            if k == 'list':     # type check
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)

        res = self.excel_result_bo.batch_delete_by_md5(params=new_params)
        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "删除结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list')) - res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list')) - res)}).json()

    def excel_init_split_params(self, params):
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
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        # check parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_init_split_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            new_params[k] = str(v)

        model = self.excel_source_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}
            ).json()

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
            for k, v in enumerate(sheet_columns_json.get(str(sheet_index))):
                column_names.append({'label': str(v) if v else '/', 'value': str(k)})
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

    def excel_sheet_header(self, params):
        """
        get sheet headers by sheet index
        params is dict
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        # check parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_sheet_header_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            v = str(v)
            if not v:       # check value is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            new_params[k] = v

        model = self.excel_source_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}
            ).json()
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
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        # init enums info
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
        new_params = dict()
        # parameters check
        for k, v in params.items():
            if not k: continue
            if k not in self.req_split_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if k == 'columns':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
            if k != 'name' and not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            if k == 'store' and v not in excel_split_store:
                return Status(
                    213, 'failure', u'请求参数%s值不合法' % k, {}
                ).json()
            elif k == 'split' and v not in excel_num:
                return Status(
                    213, 'failure', u'请求参数%s值不合法' % k, {}
                ).json()
            elif k == 'header' and v not in bool_type:
                return Status(
                    213, 'failure', u'请求参数%s值不合法' % k, {}
                ).json()

            new_params[k] = str(v) if k != 'columns' else v
        if not new_params.get('sheet'):
            new_params['sheet'] = '0'

        model = self.excel_source_bo.get_model_by_md5(md5=new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}
            ).json()
        # data is deleted
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}
            ).json()
        # authority
        rtx_id = new_params.get('rtx_id')
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                311, 'failure', StatusMsgs.get(311), {}
            ).json()
        # file not exist
        if not model.local_url or \
                not os.path.exists(model.local_url):
            return Status(
                226, 'failure', StatusMsgs.get(226), {}
            ).json()

        # 无新文件名称，以原始文件为名称
        if not new_params.get('name'):
            new_params['name'] = model.name
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
        if row == 0:
            return Status(
                227, 'failure', StatusMsgs.get(227), {}
            ).json()
        if row >= 65535:
            return Status(
                228, 'failure', StatusMsgs.get(228), {}
            ).json()

        try:    # main method
            resp_json = self.excel_lib.split_xlrw(file=model.local_url,
                                                  name=new_params.get('name'),
                                                  sheet=new_params.get('sheet'),
                                                  type=new_params.get('split'),
                                                  store=new_params.get('store'),
                                                  rule=new_params.get('columns'),
                                                  title=new_params.get('header'))
        except Exception as e:
            print('ExcelLib split excel error: %s' % e)
            return Status(
                307, 'failure', 'Excel处理split失败', {}
            ).json()

        # failure
        if resp_json.get('status_id') != 100:
            return Status(
                307, 'failure', resp_json.get('message'), {}
            ).json()
        data = resp_json.get('data')
        # file upload to store object, manual control
        store_name = '%s/%s' % (get_now('%Y%m%d'), data.get('name'))
        if EXCEL_STORE_BK:
            store_res = self.store_lib.upload(store_name=store_name, local_file=data.get('path'))
            if store_res.get('status_id') != 100:
                return Status(store_res.get('status_id'),
                              'failure',
                              store_res.get('message') or StatusMsgs.get(store_res.get('status_id')),
                              {}).json()
        # file to db
        new_data = {
            'name': data.get('name'),
            'rtx_id': new_params.get('rtx_id'),
            'store_name': store_name,
            'type': EXCEL_SPLIT,
            'md5': md5(data.get('name')),
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

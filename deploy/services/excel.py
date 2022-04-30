# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    excel service

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

from deploy.utils.status_msg import StatusMsgs
from deploy.utils.status import Status
from deploy.utils.file_lib import FileLib
from deploy.utils.store_lib import StoreLib
from deploy.utils.excel_lib import ExcelLib
from deploy.bo.excel_source import ExcelSourceBo

from deploy.config import STORE_BASE_URL, STORE_SPACE_NAME, \
    EXCEL_LIMIT, EXCEL_STORE_BK, \
    ADMIN
from deploy.utils.utils import get_now, d2s


class ExcelService(object):
    """
    excel service
    """
    req_list_attrs = [
        'rtx_id',
        'type',
        'limit',
        'offset'
    ]

    req_upload_attrs = [
        'rtx_id',
        'type'
    ]

    req_update_attrs = [
        'rtx_id',
        'name',
        'md5',
        'set_sheet'
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
        'list'
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
        'nsheet',
        'set_sheet',  # sheet_names, set_sheet_index, set_sheet_name
        # 'sheet_names',
        'create_time'
    ]

    def __init__(self):
        super(ExcelService, self).__init__()
        self.excel_lib = ExcelLib()
        self.file_lib = FileLib()
        self.store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)
        self.excel_source_bo = ExcelSourceBo()

    def get_excel_headers(self, excel_file):
        res = {'sheets': {}, 'nsheet': 0, 'names': {}, 'columns': {}}
        if not excel_file or not os.path.exists(excel_file):
            return res
        new_res = self.excel_lib.read_headers(excel_file)
        return new_res

    def store_file_to_db(self, store):
        """
        store file message to db
        params store: store message

        rtx_id: rtx-id
        type: excel type
        name: file name
        md5: file md5
        store_name: file store name
        path: file store url, no have store base url
        message: message
        """
        if not store:
            return False

        try:
            # 获取文件header
            excel_headers = self.get_excel_headers(store.get('path'))
            new_model = self.excel_source_bo.new_mode()
            new_model.rtx_id = store.get('rtx_id')
            new_model.name = store.get('name')
            new_model.store_name = store.get('store_name')
            new_model.md5_id = store.get('md5')
            new_model.ftype = store.get('type')
            new_model.local_url = store.get('path')
            new_model.store_url = store.get('store_name')
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

    def _model_to_dict(self, model):
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
            elif attr == 'url':
                if model.store_url:
                    # url
                    _res['url'] = self.store_lib.open_download_url(store_name=model.store_url)
                    # url and check
                    # resp = self.store_lib.open_download(store_name=model.store_url)
                    # _res['url'] = resp.get('data').get('url') if resp.get('status_id') == 100 else ''
                else:
                    _res['url'] = ''
            elif attr == 'nsheet':
                _res['nsheet'] = model.nsheet
            elif attr == 'set_sheet':
                if model.sheet_names:
                    new_res = list()
                    set_sheet_name = list()
                    set_sheet_index = [str(i) for i in str(model.set_sheet).split(';')] if model.set_sheet else []
                    for k, v in json.loads(model.sheet_names).items():
                        new_res.append({'key': k, 'value': v})
                        if str(k) in set_sheet_index:
                            set_sheet_name.append(v)
                    _res['sheet_names'] = new_res
                    _res['set_sheet_name'] = ';'.join(set_sheet_name)
                    _res['set_sheet_index'] = set_sheet_index
                else:
                    _res['sheet_names'] = []
                    _res['set_sheet_index'] = []
                    _res['set_sheet_name'] = ''
            elif attr == 'create_time':
                _res['create_time'] = d2s(model.create_time) if model.create_time else ''
        else:
            return _res

    def excel_list(self, params):
        """
        get excel list by type and (source or result)
        params is dict
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_list_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if k == 'limit':
                new_params[k] = int(v) if v else EXCEL_LIMIT
            elif k == 'offset':
                new_params[k] = int(v) if v else 0
            else:
                new_params[k] = v
        new_params['enum_name'] = 'excel-type'
        res, total = self.excel_source_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}
            ).json()

        new_res = list()
        for _d in res:
            if not _d: continue
            new_res.append(self._model_to_dict(_d))
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def excel_upload(self, params, upload_file, is_check_fmt: bool = True):
        """
        one file to upload
        params params: request params, rtx_id and excel type
        params upload_file: excel upload file
        params is_check_fmt: file is or not check format
        params is_store_bk: file is or not upload to store server 对象存储备份

        excel upload to qiniu store server
        1.local store
        2.upload to qiniu store server
        """
        if not params:
            return Status(
                212, 'failure', u'缺少请求参数', {}
            ).json()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_upload_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
        if not params.get('rtx_id'):
            return Status(
                212, 'failure', u'缺少rtx_id请求参数', {}
            ).json()
        if not params.get('type'):
            return Status(
                212, 'failure', u'未指定type请求参数', {}
            ).json()

        f_name = upload_file.filename
        # file format filter
        if is_check_fmt and not self.file_lib.allow_format_fmt(f_name):
            return Status(
                217, 'failure', StatusMsgs.get(217), {}
            ).json()
        # file local store
        is_ok, store_msg = self.file_lib.store_file(upload_file, compress=False, is_md5_store_name=False)
        if not is_ok:
            return Status(
                220, 'failure', StatusMsgs.get(220), {}
            ).json()
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
        store_msg['type'] = params.get('type')
        is_to_db = self.store_file_to_db(store_msg)
        if not is_to_db:
            return Status(
                225, 'failure', StatusMsgs.get(225), {}
            ).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {}
        ).json()

    def excel_upload_m(self, params, upload_files, is_check_fmt: bool = True):
        """
        many file to upload
        params params: request params
        params upload_files: excel upload file
        params is_check_fmt: file is or not check format

        excel upload to qiniu store server
        1.local store
        2.upload to qiniu store server
        """
        if not params:
            return Status(
                212, 'failure', u'缺少请求参数', {}
            ).json()

        success_list = list()
        failure_list = list()
        for uf in upload_files:
            try:
                if not uf: continue
                store_res = self.excel_upload(params=params, upload_file=upload_files.get(uf))
                store_res_json = json.loads(store_res)
                success_list.append(uf) if store_res_json.get('status_id') == 100 \
                    else failure_list.append(uf)
            except:
                failure_list.append(uf)
        if upload_files and len(failure_list) == len(upload_files):
            return Status(
                223, 'failure', '文件上传失败' or StatusMsgs.get(223), {}
            ).json()
        if failure_list:
            return Status(
                224, 'failure', u'文件上传成功：%s，失败：%s' % (len(success_list), len(failure_list)),
                {}
            ).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {}
        ).json()

    def excel_update(self, params):
        """
        get excel list by type and (source or result)
        params is dict
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_update_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            if k == 'set_sheet':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                new_params[k] = ';'.join(v)
            else:
                new_params[k] = str(v)

        model = self.excel_source_bo.get_model_by_md5(md5=new_params.get('md5'))
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}
            ).json()
        if model and model.is_del:
            return Status(
                304, 'failure', StatusMsgs.get(304), {}
            ).json()
        rtx_id = new_params.get('rtx_id')
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                310, 'failure', StatusMsgs.get(310), {}
            ).json()
        if new_params.get('name'):
            model.name = new_params.get('name')
        if new_params.get('set_sheet'):
            model.set_sheet = new_params.get('set_sheet')
        self.excel_source_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def excel_delete(self, params):
        """
        delete excel file by params
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
        if not model:
            return Status(
                302, 'failure', StatusMsgs.get(302), {}
            ).json()
        if model and model.is_del:
            return Status(
                306, 'failure', StatusMsgs.get(306), {}
            ).json()
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

    def excel_deletes(self, params):
        """
        delete many excel file by params
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
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            if k == 'list':
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
            else Status(303, 'success', StatusMsgs.get(303), {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def excel_merge(self, params):
        """
        many file to merge one file
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
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            if k == 'list':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s类型必须是List' % k, {}
                    ).json()
                new_params[k] = [str(i) for i in v]
            else:
                new_params[k] = str(v)
                
        return Status(
            100, 'success', StatusMsgs.get(100), {}
        ).json()

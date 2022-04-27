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

from deploy.config import STORE_BASE_URL, STORE_SPACE_NAME
from deploy.utils.utils import get_now


class ExcelService(object):
    """
    excel service
    """
    upload_attrs = ['rtx_id', 'token', 'type']

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
            # 设置默认第一个Sheet进行操作
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

    def excel_upload(self, params, upload_file, is_check_fmt: bool = True):
        """
        one file to upload
        params params: request params, rtx_id and excel type
        params upload_file: excel upload file
        params is_check_fmt: file is or not check format

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
            if k not in self.upload_attrs:
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
        # file upload to store object
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
        # if not is_to_db:
        #     return Status(
        #         220, 'failure', StatusMsgs.get(220), {}
        #     ).json()

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
            if not uf: continue
            store_res = self.excel_upload(params=params, upload_file=upload_files.get(uf))
            store_res_json = json.loads(store_res)
            success_list.append(uf) if store_res_json.get('status_id') == 100 \
                else failure_list.append(uf)
            try:
                pass
            except:
                failure_list.append(uf)
        if upload_files and len(failure_list) == len(upload_files):
            return Status(
                223, 'failure', '文件上传失败 --------' or StatusMsgs.get(223), {}
            ).json()
        if failure_list:
            return Status(
                224, 'failure', u'文件上传成功：%s，失败：%s' % (len(success_list), len(failure_list)),
                {}
            ).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {}
        ).json()

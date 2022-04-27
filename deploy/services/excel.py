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
import json

from deploy.utils.status_msg import StatusMsgs
from deploy.utils.status import Status
from deploy.utils.file_lib import FileLib
from deploy.utils.store_lib import StoreLib

from deploy.config import STORE_BASE_URL, STORE_SPACE_NAME


class ExcelService(object):
    def __init__(self):
        super(ExcelService, self).__init__()
        self.file_lib = FileLib()
        self.store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)

    def excel_upload(self, rtx_id: str, upload_file, is_check_fmt: bool = True):
        """
        one file to upload
        params rtx_id: rtx id
        params upload_file: excel upload file
        params is_check_fmt: file is or not check format

        excel upload to qiniu store server
        1.local store
        2.upload to qiniu store server
        """
        if not rtx_id:
            return Status(
                212, 'failure', u'缺少rtx_id请求参数', {}
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
        # is_to_db = self.__store_file_to_db(store_msg)
        return Status(
            100, 'success', StatusMsgs.get(100), {}
        ).json()

    def excel_upload_m(self, rtx_id: str, upload_files, is_check_fmt: bool = True):
        """
        many file to upload
        params rtx_id: rtx id
        params upload_files: excel upload file
        params is_check_fmt: file is or not check format

        excel upload to qiniu store server
        1.local store
        2.upload to qiniu store server
        """
        if not rtx_id:
            return Status(
                212, 'failure', u'缺少rtx_id请求参数', {}
            ).json()

        success_list = list()
        failure_list = list()
        for uf in upload_files:
            if not uf: continue
            try:
                store_res = self.excel_upload(rtx_id=rtx_id, upload_file=upload_files.get(uf))
                store_res_json = json.loads(store_res)
                success_list.append(uf) if store_res_json.get('status_id') == 100 \
                    else failure_list.append(uf)
            except:
                failure_list.append(uf)
        if upload_files and len(failure_list) == len(upload_files):
            return Status(
                223, 'failure', StatusMsgs.get(223), {}
            ).json()
        if failure_list:
            return Status(
                224, 'failure', u'文件上传成功：%s，失败：%s' % (len(success_list), len(failure_list)),
                {}
            ).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {}
        ).json()

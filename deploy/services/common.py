# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/7/18 20:45"
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
# usage: /usr/bin/python common.py
# ------------------------------------------------------------
import json

from deploy.utils.status_msg import StatusMsgs
from deploy.utils.status import Status
from deploy.delibs.file_lib import FileLib
from deploy.delibs.store_lib import StoreLib
from deploy.services.office import OfficeService
from deploy.services.notify import NotifyService
from deploy.delibs.image_lib import ImageLib

from deploy.config import STORE_BASE_URL, STORE_SPACE_NAME, OFFICE_STORE_BK
from deploy.utils.enums import *
from deploy.utils.utils import get_now


class CommonService(object):
    """
    common service
    """

    req_upload_attrs = [
        'rtx_id',
        'file_type'
    ]

    req_upload_need_attrs = [
        'rtx_id',
        'file_type'
    ]

    def __init__(self):
        """
        common service class initialize
        """
        super(CommonService, self).__init__()
        self.file_lib = FileLib()
        self.store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)
        self.office_service = OfficeService()
        self.notify_service = NotifyService()
        self.image_lib = ImageLib()

    def file_upload(self, params, upload_file, is_check_fmt: bool = True) -> json:
        """
        one file upload to server(file store object)
        params params: request params, rtx_id and file type
        params upload_file: upload file
        params is_check_fmt: file is or not check format
        params is_store_bk: file is or not upload to store server 对象存储备份

        file upload to qiniu store server
        1.local store
        2.upload to qiniu store server

        return json data

        获取不同模型的service，进行操作
        """
        # ------------------------ parameters check -----------------------
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
            # necessary value check
            if not v and k in self.req_upload_attrs:
                return Status(
                    212, 'failure', u'缺少%s请求参数' % k, {}
                ).json()

        # ======================= local store =======================
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
        # ======================= 【云存储】 =======================
        # file upload to store object
        store_res = self.store_lib.upload(store_name=store_msg.get('store_name'),
                                          local_file=store_msg.get('path'))
        if store_res.get('status_id') != 100:
            return Status(store_res.get('status_id'),
                          'failure',
                          store_res.get('message') or StatusMsgs.get(store_res.get('status_id')),
                          {}).json()

        # ======================= db store =======================
        store_msg['rtx_id'] = params.get('rtx_id')
        store_msg['file_type'] = params.get('file_type')
        # 存储文件记录到数据库，依据file_type进行不同存储
        file_type = int(params.get('file_type'))
        if file_type in [FileTypeEnum.EXCEL_MERGE.value,
                         FileTypeEnum.EXCEL_SPLIT.value]:   # excel merge && split
            is_to_db = self.office_service.store_excel_source_to_db(store_msg)
        elif file_type == FileTypeEnum.WORD.value:  # word
            pass
        elif file_type == FileTypeEnum.PPT.value:   # ppt
            pass
        elif file_type == FileTypeEnum.TEXT.value:   # text
            pass
        elif file_type == FileTypeEnum.PDF.value:   # office pdf
            is_to_db = self.office_service.store_office_pdf_to_db(store_msg)
        elif file_type == FileTypeEnum.DTALK.value:   # notify dtalk
            is_to_db = self.notify_service.store_dtalk_to_db(store_msg)
        else:   # other
            pass
        if not is_to_db:
            return Status(
                225, 'failure', StatusMsgs.get(225), {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {}).json()

    def file_uploads(self, params, upload_files, is_check_fmt: bool = True) -> json:
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
        # ------------------------ upload start -----------------------
        # TODO 循环的方式进行存储文件，后期改成多进程
        for uf in upload_files:
            try:
                if not uf: continue
                store_res = self.file_upload(params=params, upload_file=upload_files.get(uf))
                store_res_json = json.loads(store_res)
                success_list.append(uf) if store_res_json.get('status_id') == 100 \
                    else failure_list.append(uf)
            except:
                failure_list.append(uf)
        # ------------------------ upload end -----------------------
        if upload_files and len(failure_list) == len(upload_files):
            return Status(
                223, 'failure', '文件上传失败' or StatusMsgs.get(223), {}).json()
        if failure_list:
            return Status(
                224, 'failure', u'文件上传：成功[%s]，失败[%s]' % (len(success_list), len(failure_list)),
                {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {}).json()

    def image_wangeditor(self, params, image_file) -> dict:
        """
        wang editor image upload load image to server
        params: parameters
        image_file: image file object

        no database record, but to upload qiniu server

        response格式说明：
        正确：
        {
            "errno": 0, // 注意：值是数字，不能是字符串
            "data": {
                "url": "xxx", // 图片 src ，必须
                "alt": "yyy", // 图片描述文字，非必须
                "href": "zzz" // 图片的链接，非必须
            }
        }
        错误：
        {
            "errno": 1, // 只要不等于 0 就行
            "message": "失败信息"
        }
        """
        # check parameters
        if not params:
            return {'errno': 212, 'message': '缺少请求参数'}
        if not image_file:
            return {'errno': 212, 'message': '缺少上传文件'}

        try:
            image_name = image_file.filename
            # ============= image format check =============
            if not self.image_lib.allow_format_img(image_name):
                return {'errno': 401, 'message': '图片格式不支持'}
            # ============= local store =============
            local_res = self.image_lib.store_local(image_file, compress=False)
            if local_res.get('status_id') != 100:
                return {
                    'errno': local_res.get('status_id'),
                    'message': local_res.get('message') or '本地存储失败'
                }
            local_image_file = local_res.get('data').get('file')
            # TODO 判断图片大小限制
            # image_info = self.image_lib.scan(local_image_file)

            # ============= upload store =============
            store_image_name = '%s/%s' % (get_now(format="%Y%m%d"), local_res.get('data').get('name'))
            store_res = self.store_lib.upload(store_name=store_image_name, local_file=local_image_file)
            if store_res.get('status_id') != 100:
                return {
                    'errno': local_res.get('status_id'),
                    'message': local_res.get('message') or '云存储失败'
                }
            # ---------------- return server url ----------------
            image_url = store_res.get('data').get('url')
            image_alt = str(image_name).split('.')[0]
            return {
                "errno": 0,
                "data": {
                    "url": image_url,
                    "alt": image_alt
                    # "href": _url
                }
            }
        except Exception as e:
            return {'errno': 501, 'message': '服务端API请求发生故障，请稍后尝试' or e}




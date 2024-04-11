# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    common service

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

# lib
from deploy.delib.file_lib import FileLib
from deploy.delib.store_lib import StoreLib
from deploy.delib.image_lib import ImageLib
# service
from deploy.service.office import OfficeService
from deploy.service.notify import NotifyService
from deploy.service.search import SearchService
from deploy.service.info import InfoService
from deploy.service.authority import AuthorityService
# bo
from deploy.bo.enum import EnumBo

from deploy.config import STORE_BASE_URL, STORE_SPACE_NAME, OFFICE_STORE_BK
from deploy.utils.enum import *
from deploy.utils.utils import get_now, check_length, auth_rtx_join
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.status import Status


class CommonService(object):
    """
    common service
    """

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

    req_upload_attrs = [
        'rtx_id',
        'file_type'
    ]

    req_upload_need_attrs = [
        'rtx_id',
        'file_type'
    ]

    req_download_excel_attrs = [
        'rtx_id',
        'source',
        'list',
        'file_name',
        'file_type',
        'file_format'
    ]

    req_download_excel_need_attrs = [
        'rtx_id',
        'source',
        'file_name',
        'file_type',
        'file_format'
    ]

    req_download_excel_check_length_attrs = {
        'file_name': 55
    }

    EXCEL_SUFFIX = ['xls', 'xlsx']
    DOWNLOAD_TYPE = ['All', 'Select']
    DOWNLOAD_NO_SELECT = ['system-depart', 'manage-menu']

    def __init__(self):
        """
        CommonService class initialize
        """
        super(CommonService, self).__init__()
        # lib
        self.file_lib = FileLib()
        self.store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)
        self.image_lib = ImageLib()
        # service
        self.office_service = OfficeService()
        self.notify_service = NotifyService()
        self.search_service = SearchService()
        self.info_service = InfoService()
        self.authority_service = AuthorityService()
        # bo
        self.enum_bo = EnumBo()

    def __str__(self):
        print("CommonService class.")

    def __repr__(self):
        self.__str__()

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
                400, StatusEnum.FAILURE.value, StatusMsgs.get(400), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_upload_attrs:
            if _attr not in params.keys():
                return Status(
                    400, StatusEnum.FAILURE.value, '缺少请求参数%s' % _attr, {}).json()
        """end"""
        # **************************************************************************
        for k, v in params.items():
            if not k: continue
            # illegal parameters check
            if k not in self.req_upload_attrs:
                return Status(
                    401, StatusEnum.FAILURE.value, '请求参数%s不合法' % k, {}).json()
            # necessary value check
            if not v and k in self.req_upload_attrs:
                return Status(
                    403, StatusEnum.FAILURE.value, '请求参数%s不允许为空' % k, {}).json()

        f_name = getattr(upload_file, 'filename')   # file public object
                                                    # use getattr method to get file name
        # ======================= local store =======================
        # file format filter
        if is_check_fmt and not self.file_lib.allow_format_fmt(f_name):
            return Status(
                454, StatusEnum.FAILURE.value, "文件格式不支持", {}).json()
        # file local store
        is_ok, store_msg = self.file_lib.store_file(
            upload_file, compress=False, is_md5_store_name=False)
        if not is_ok:
            return Status(
                456, StatusEnum.FAILURE.value, "文件本地存储失败", {}).json()
        # ======================= 【云存储】 =======================
        # file upload to store object
        store_res = self.store_lib.upload(store_name=store_msg.get('store_name'),
                                          local_file=store_msg.get('path'))
        if store_res.get('status_id') != 100:
            return Status(store_res.get('status_id') or 902,
                          StatusEnum.FAILURE.value,
                          store_res.get('message') or "第三方[七牛云存储]API接口异常",
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
                601, StatusEnum.FAILURE.value, "数据库新增数据失败", {}).json()

        return Status(
            100, StatusEnum.SUCCESS.value, StatusMsgs.get(100), {}).json()

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
                400, StatusEnum.FAILURE.value, '缺少请求参数', {}).json()

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
                460, StatusEnum.FAILURE.value, '文件上传失败', {}).json()
        if failure_list:
            return Status(
                461,
                StatusEnum.FAILURE.value,
                '文件上传：成功[%s]，失败[%s]' % (len(success_list), len(failure_list)),
                {}).json()

        return Status(
            100, StatusEnum.SUCCESS.value, StatusMsgs.get(100), {}).json()

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
            return {'errno': 400, 'message': '缺少请求参数'}
        if not image_file:
            return {'errno': 450, 'message': '缺少上传文件'}

        try:
            image_name = image_file.filename
            # ============= image format check =============
            if not self.image_lib.allow_format_img(image_name):
                return {'errno': 454, 'message': '图片格式不支持'}
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
            return {'errno': 900, 'message': '服务端API请求发生异常，请稍后尝试' or e}

    def download_excel_init(self, params):
        # ------------------------ parameters check -----------------------
        # no parameters
        if not params:
            return Status(
                400, StatusEnum.FAILURE.value, StatusMsgs.get(400), {}).json()

        rtx_id = params.get('rtx_id')
        if not rtx_id:
            return Status(
                4001, StatusEnum.FAILURE.value, '缺少RTX-ID请求参数', {}).json()
        # ------------------------ parameters check -----------------------
        enum_names = ['download-select', 'excel-format']
        res = self.enum_bo.get_model_by_names(names=enum_names)
        download_select_list = list()
        excel_format_list = list()
        for e in res:
            if not e: continue
            if e.name == 'download-select':
                download_select_list.append({'name': str(e.name), 'label': str(e.value), 'value': str(e.key)})
            elif e.name == 'excel-format':
                excel_format_list.append({'name': str(e.name), 'label': str(e.value), 'value': str(e.key)})
        data = {
            'download_select': download_select_list,
            'excel_format': excel_format_list
        }
        return Status(
            100, StatusEnum.SUCCESS.value, StatusMsgs.get(100), data).json()

    def download_excel(self, params):
        # ------------------------ parameters check -----------------------
        # no parameters
        if not params:
            return Status(
                400, StatusEnum.FAILURE.value, StatusMsgs.get(400), {}).json()

        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_download_excel_attrs:
            if _attr not in params.keys():
                return Status(
                    400, StatusEnum.FAILURE.value, '缺少请求参数%s' % _attr, {}).json()
        """end"""
        # **************************************************************************

        # ===================== parameters check and format =====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_download_excel_attrs:     # illegal key
                return Status(
                    401, StatusEnum.FAILURE.value, '请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if k in self.req_download_excel_need_attrs and not v:
                return Status(
                    403, StatusEnum.FAILURE.value, '请求参数%s不允许为空' % k, {}).json()
            # parameters check
            if k == 'list':    # parameter type check
                if not isinstance(v, list):
                    return Status(
                        402, StatusEnum.FAILURE.value, '请求参数%s类型需要是List' % k, {}).json()
                new_params[k] = v
            else:
                new_params[k] = str(v)

        # parameters length check
        for _key, _value in self.req_download_excel_check_length_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    405, StatusEnum.FAILURE.value, '请求参数%s长度超出限制' % _key, {}).json()
        # parameters enum check
        file_format = new_params.get('file_format')
        if file_format not in self.EXCEL_SUFFIX:
            return Status(
                404, StatusEnum.FAILURE.value, '请求参数file_format只支持xls，xlsx枚举值', {}).json()
        # 依据type：All全部数据 Select选择数据
        file_type = new_params.get('file_type')
        if file_type not in self.DOWNLOAD_TYPE:
            return Status(
                404, StatusEnum.FAILURE.value, '请求参数type只支持All，Select枚举值', {}).json()
        # Select选择数据的时候需要提供下载数据的list列表
        # 特殊无选择功能不支持选择性数据下载
        if file_type == 'Select' \
                and not new_params.get('list') \
                and new_params.get('source') not in self.DOWNLOAD_NO_SELECT:
            return Status(
                403, StatusEnum.FAILURE.value, '请求参数list不允许为空', {}).json()
        elif file_type == 'All':
            # 如果是全部下载，删除list参数
            del new_params['list']
        # 根据用户权限下载数据，管理权限允许下载全部数据
        rtx_id = new_params.get('rtx_id')
        if rtx_id in auth_rtx_join([]):
            del new_params['rtx_id']

        # 文件名称
        file_all_name = '%s.%s' % (new_params.get('file_name'), file_format)
        # 数据下载请求对应的service
        source = new_params.get('source')
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if source == 'office-pdf':
            # 文档工具 > PDF转WORD
            res = self.office_service.pdf_2_word_download(params=new_params)
        elif source == 'office-excel-source-merge':
            # 文档工具 > 表格合并
            # 1-excel merge, 2-excel split
            new_params['type'] = 1
            new_params['enum_name'] = 'excel-type'
            res = self.office_service.excel_source_download(params=new_params)
        elif source == 'office-excel-source-split':
            # 文档工具 > 表格拆分
            # 1-excel merge, 2-excel split
            new_params['type'] = 2
            new_params['enum_name'] = 'excel-type'
            res = self.office_service.excel_source_download(params=new_params)
        elif source == 'office-excel-result':
            # 文档工具 > 表格历史
            new_params['enum_name'] = 'excel-type'
            res = self.office_service.excel_result_download(params=new_params)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        elif source == 'search-sqlbase':
            # 知识平台 > SQL仓库
            new_params['enum_name'] = 'db-type'   # 数据库枚举RTX
            new_params['public'] = 1           # 已发布
            res = self.search_service.sqlbase_download(params=new_params)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        elif source == 'notify-dtalk':
            # 消息通知 > 钉钉绩效
            res = self.notify_service.dtalk_download(params=new_params)
        elif source == 'notify-qywx':
            # 消息通知 > 企微通知
            new_params['enum_name'] = 'qywx-type'   # 数据库枚举RTX
            res = self.notify_service.qywx_download(params=new_params)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        elif source == 'system-depart':
            # 系统维护 > 部门架构
            res = self.info_service.depart_download(params=new_params)
        elif source == 'system-dict':
            # 系统维护 > 数据字典
            res = self.info_service.dict_download(params=new_params)
        elif source == 'system-api':
            # 系统维护 > 后台API
            res = self.info_service.api_download(params=new_params)
        elif source == 'system-log':
            # 系统维护 > 日志查看
            res = self.info_service.log_download(params=new_params)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        elif source == 'manage-user':
            # 权限管理 > 用户管理
            res = self.authority_service.user_download(params=new_params)
        elif source == 'manage-role':
            # 权限管理 > 角色管理
            res = self.authority_service.role_download(params=new_params)
        elif source == 'manage-menu':
            # 权限管理 > 菜单管理
            res = self.authority_service.menu_download(params=new_params)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        else:
            return Status(
                401,
                StatusEnum.SUCCESS.value,
                "暂无资源下载",
                {'list': [], 'total': 0, 'name': file_all_name}
            ).json()

        status_id = 100 if len(res) > 0 else 101
        return Status(
            status_id,
            StatusEnum.SUCCESS.value,
            StatusMsgs.get(100),
            {'list': res, 'total': len(res), 'name': file_all_name}
        ).json()

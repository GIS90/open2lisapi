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
import time
import random

from deploy.delibs.excel_lib import ExcelLib
from deploy.utils.utils import get_now, d2s, check_length, md5, auth_rtx_join
from deploy.bo.dtalk_message import DtalkMessageBo
from deploy.bo.dtalk_robot import DtalkRobotBo
from deploy.bo.qywx_message import QywxMessageBo
from deploy.bo.qywx_robot import QywxRobotBo
from deploy.bo.enum import EnumBo
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.config import OFFICE_LIMIT, SHEET_NUM_LIMIT, SHEET_NAME_LIMIT, \
    STORE_BASE_URL, STORE_SPACE_NAME, \
    DTALK_CONTROL, DTALK_INTERVAL, DTALK_ADD_IMAGE, AUTH_NUM
from deploy.delibs.store_lib import StoreLib
from deploy.delibs.dtalk_lib import DtalkLib
from deploy.delibs.qywx_lib import QYWXLib
from deploy.delibs.file_lib import FileLib


class NotifyService(object):
    """
    notify service
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
        'file_type',
        'excel_sub_type'
    ]

    req_delete_attrs = [
        'rtx_id',
        'md5'
    ]

    req_deletes_attrs = [
        'rtx_id',
        'list'
    ]

    req_detail_attrs = [
        'rtx_id',
        'md5'
    ]

    req_dtalk_update_attrs = [
        'rtx_id',
        'name',
        'set_sheet',
        'cur_sheet',
        'title',
        'column',
        'md5'
    ]

    req_dtalk_update_need_attrs = [
        'rtx_id',
        'name',
        'set_sheet',
        'cur_sheet',
        'column',
        'md5'
    ]

    req_change_sheet_attrs = [
        'rtx_id',
        'md5',
        'sheet'
    ]

    dtalk_list_attrs = [
        'id',
        'rtx_id',
        'file_name',
        'url',  # 'file_local_url', 'file_store_url',
        'md5_id',
        'robot',
        'count',
        'number',
        'nsheet',
        'set_sheet',
        'cur_sheet',
        'set_column',
        'set_title',
        'create_time',
        'delete_rtx',
        'delete_time',
        'is_del'
    ]

    dtalk_detail_attrs = [
        'id',
        'rtx_id',
        'file_name',
        'url',  # 'file_local_url', 'file_store_url',
        'md5_id',
        'robot',
        'count',
        'number',
        'nsheet',
        # 'sheet_names',
        # 'sheet_columns',
        # 'headers',
        'set_sheet',
        'cur_sheet',
        'cur_set_column',
        'cur_set_title',
        'create_time',
        'delete_rtx',
        'delete_time',
        'is_del'
    ]

    dtalk_robot_attrs = [
        # 'id',
        'rtx_id',
        'name',
        'md5_id',
        'key',
        'secret',
        'select',
        'description',
        'create_time',
        'delete_rtx',
        'delete_time',
        'is_del'
    ]

    dtalk_robot_add_attrs = [
        'rtx_id',
        'name',
        'key',
        'secret',
        'description',
        'select'
    ]

    dtalk_robot_add_ck_len_attrs = {
        'rtx_id': 25,
        'name': 30,
        'key': 30,
        'secret': 70
    }

    req_dtalk_robot_update_attrs = [
        'rtx_id',
        'name',
        'key',
        'secret',
        'description',
        'select',
        'md5'
    ]

    req_dtalk_robot_select_attrs = [
        'rtx_id',
        'md5',
        'select'
    ]

    req_dtalk_robot_ping_attrs = [
        'rtx_id',
        'md5'
    ]

    req_dtalk_send_init_attrs = [
        'rtx_id',
        'md5'
    ]

    req_dtalk_send_attrs = [
        'rtx_id',
        'robot',
        'sheet',
        'md5'
    ]

    qywx_robot_attrs = [
        # 'id',
        'rtx_id',
        'name',
        'md5_id',
        'key',
        'secret',
        'agent',
        'select',
        'description',
        'create_time',
        'delete_rtx',
        'delete_time',
        'is_del'
    ]

    qywx_robot_add_attrs = [
        'rtx_id',
        'name',
        'key',
        'secret',
        'agent',
        'description',
        'select'
    ]

    qywx_robot_attrs_length_check = {
        'rtx_id': 25,
        'name': 30,
        'key': 30,
        'secret': 70,
        'agent': 8,
        'description': 120
    }

    req_qywx_robot_update_attrs = [
        'rtx_id',
        'name',
        'key',
        'secret',
        'agent',
        'description',
        'select',
        'md5'
    ]

    req_qywx_robot_select_attrs = [
        'rtx_id',
        'md5',
        'select'
    ]

    req_qywx_robot_ping_attrs = [
        'rtx_id',
        'md5'
    ]

    qywx_list_attrs = [
        'id',
        'rtx_id',
        'title',
        'content',
        'user',
        'md5_id',
        'robot',
        'type',
        'count',
        'last_send_time',
        'create_time',
        'delete_rtx',
        'delete_time',
        'is_del',
        # 'enum_name',
        # 'enum_key',
        'enum_value',
        'is_back',
        'msg_id'
    ]

    req_qywx_add_attrs = [
        'rtx_id',
        'title',
        'content',
        'user',
        'type',
        'robot'
    ]

    req_qywx_add_length_check = {
        'title': 55,
        'content': 1000,
        'user': 10000   # 最大用户1000个，字符ID名称限制字符10000个
    }

    req_qywx_update_attrs = [
        'rtx_id',
        'title',
        'content',
        'user',
        'type',
        'robot',
        'md5'
    ]

    req_qywx_send_attrs = [
        'rtx_id',
        'title',
        'content',
        'user',
        'type',
        'robot',
        'md5'
    ]

    req_qywx_send_temp_send_attrs = [
        'md5',
        'temp'
    ]

    req_send_temp_attrs = [
        'rtx_id'
    ]

    req_qywx_send_temp_attrs = [
        'rtx_id',
        'title',
        'content',
        'user',
        'type',
        'robot'
    ]

    req_qywx_backsend_attrs = [
        'rtx_id',
        'md5'
    ]

    req_qywx_temp_upload_attrs = [
        'rtx_id',
        'robot',
        'type'
    ]

    EXCEL_FORMAT = ['.xls', '.xlsx']

    DEFAULT_EXCEL_FORMAT = '.xlsx'

    temp_upload_types = [
        'image',  # 图片
        'voice',  # 语音
        'video',  # 视频
        'file',  # 普通文件
    ]

    def __init__(self):
        """
        notify service class initialize
        """
        super(NotifyService, self).__init__()
        # Lib
        self.excel_lib = ExcelLib()
        self.store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)
        self.file_lib = FileLib()
        # Bo
        self.dtalk_bo = DtalkMessageBo()
        self.dtalk_robot_bo = DtalkRobotBo()
        self.qywx_bo = QywxMessageBo()
        self.qywx_robot_bo = QywxRobotBo()
        self.enum_bo = EnumBo()

    @staticmethod
    def _transfer_time(t):
        if not t:
            return ""

        if not isinstance(t, str):
            return d2s(t)
        elif isinstance(t, str) and t == '0000-00-00 00:00:00':
            return ""
        else:
            return t or ''

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

    def _default_columns(self, columns):
        """
        build in method to format column
        all select

        columns is dict
        return is dict
        """
        if not columns:
            return {}

        _res = dict()
        for k, v in columns.items():
            if not str(k) or not v: continue
            _d = list()
            for _v_v in v:
                if not _v_v or not _v_v.get('key'): continue
                _d.append(str(_v_v.get('key')))
            _res[k] = _d
        return _res

    def store_dtalk_to_db(self, store):
        """
        store dtalk excel source file message to db
        params store: store message
            - rtx_id: rtx-id
            - file_type: file type
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
            new_model.cur_sheet = '0'
            new_model.sheet_names = json.dumps(excel_headers.get('names'))
            new_model.sheet_columns = json.dumps(excel_headers.get('columns'))
            new_model.headers = json.dumps(excel_headers.get('sheets'))
            new_model.set_column = json.dumps(self._default_columns(excel_headers.get('columns') or {}))   # 默认设置全部
            new_model.set_title = json.dumps({})   # title默认设置全部为空
            new_model.create_time = get_now()
            new_model.is_del = False
            self.dtalk_bo.add_model(new_model)
            return True
        except:
            return False

    def _update_real_file_name(self, model, new_name):
        """
        build in method, not allow outer to use
        update file name store_name local_url store_url
        return json data

        update real file name and store file name
        """
        _res = dict()
        # check
        if not model or not new_name:
            return _res
        if not model.file_name \
                or not model.file_local_url or not model.file_store_url:
            return _res

        new_names = os.path.splitext(str(new_name))
        # check format
        if new_names[-1] not in self.EXCEL_FORMAT:
            new_name = '%s%s' % (new_names[0], self.DEFAULT_EXCEL_FORMAT)
        local_urls = str(model.file_local_url).split('/')
        new_local_url = str(model.file_local_url).replace(local_urls[-1], new_name)
        # check rename file exist
        if os.path.exists(new_local_url):
            new_names = os.path.splitext(str(new_name))
            new_name = '%s-%s%s' % (new_names[0], get_now(format="%Y-%m-%d-%H-%M-%S"), new_names[-1])
            new_local_url = str(model.file_local_url).replace(local_urls[-1], new_name)
        # modify file name
        if os.path.exists(model.file_local_url):
            os.rename(model.file_local_url, new_local_url)
        # store file rename
        try:
            store_urls = str(model.file_store_url).split('/')
            new_store_url = str(model.file_store_url).replace(store_urls[-1], new_name)
            _store_rename_res = self.store_lib.move(src_space_name=STORE_SPACE_NAME, src_store_name=model.file_store_url,
                                                    tar_space_name=STORE_SPACE_NAME, tar_store_name=new_store_url)
            if _store_rename_res.get('status_id') != 100:
                new_store_url = model.file_store_url
        except:
            new_store_url = model.file_store_url
        return {
            'name': new_name,
            'local_url': new_local_url,
            'store_url': new_store_url
        }

    def _dtalk_model_to_dict(self, model, _type='list'):
        """
        dtalk model to dict
        params model: dtalk model object
        attrs from class define attrs
        return dict data

        type is list table show data
        type is detail data detail and config
        """
        _res = dict()
        if not model:
            return _res

        _attrs = self.dtalk_detail_attrs \
            if _type == 'detail' else self.dtalk_list_attrs
        for attr in _attrs:
            if not attr: continue
            if attr == 'id':
                _res[attr] = getattr(model, 'id', '')
            elif attr == 'rtx_id':
                _res[attr] = getattr(model, 'rtx_id', '')
            elif attr == 'file_name':
                _res[attr] = getattr(model, 'file_name', '')
            elif attr == 'md5_id':
                _res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'robot':
                _res[attr] = getattr(model, 'robot', '')
            elif attr == 'count':
                _res[attr] = getattr(model, 'count', 0)
            elif attr == 'number':
                _res[attr] = getattr(model, 'number', 0)
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
                _res['nsheet'] = getattr(model, 'nsheet', 1)  # 无值，默认为1个SHEET
            elif attr == 'set_sheet':
                """
                set_sheet_name：字符串，选择的sheet名称（拼接）
                sheet_names: 列表类型，元素为{'key': k, 'value': v}格式
                set_sheet_index：列表类型，选择的sheet列表，与sheet_names搭配显示select多选
                """
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
                    # fix bug: 详情sheet_headers的条数限制问题
                    if _type in ['list'] and len(set_sheet_name) > SHEET_NAME_LIMIT:  # 加了展示字数的限制，否则页面展示太多
                        set_sheet_name = '%s...具体查看请下载' % set_sheet_name[0:SHEET_NAME_LIMIT]
                    _res['set_sheet_name'] = set_sheet_name
                    _res['set_sheet_index'] = set_sheet_index
                else:
                    _res['sheet_names'] = []
                    _res['set_sheet_index'] = []
                    _res['set_sheet_name'] = ''
            elif attr == 'cur_sheet':
                _res[attr] = str(getattr(model, 'cur_sheet', 0))
            elif attr == 'set_column':
                _res[attr] = getattr(model, 'set_column', "")
            elif attr == 'set_title':
                _title = '暂无消息标题'
                title_json = json.loads(model.set_title) if model.set_title else {}
                sheet_names_json = json.loads(model.sheet_names) or {}
                # 无title and sheet names
                if not title_json and not sheet_names_json:
                    _res[attr] = _title
                    continue
                _str_title = ''
                if sheet_names_json:
                    for k, v in sheet_names_json.items():
                        if not str(k): continue
                        _str_title += '【%s】：%s｜' % (v or "Sheet", title_json.get(str(k)) or _title)
                else:
                    for k, v in title_json.items():
                        if not str(k): continue
                        _str_title += '【%s】：%s｜' % (k or "Sheet", title_json.get(str(k)) or _title)
                _str_title = _str_title[0:-1]   # 去掉尾部｜
                if len(_str_title) > SHEET_NAME_LIMIT:  # 加了展示字数的限制，否则页面展示太多
                    _str_title = '%s...具体详情查看设置' % _str_title[0:SHEET_NAME_LIMIT]
                _res[attr] = _str_title
            elif attr == 'cur_set_column':
                all_column_json = json.loads(model.sheet_columns)
                _set_column_json = json.loads(model.set_column)
                cur_sheet = str(model.cur_sheet) if model.cur_sheet else "0"
                _res['set_select_column'] = [] if not _set_column_json \
                    else _set_column_json.get(cur_sheet) or []
                _res['set_columns'] = all_column_json.get(cur_sheet) if all_column_json \
                    else []
            elif attr == 'cur_set_title':
                title_json = json.loads(model.set_title) if model.set_title else {}
                cur_sheet = str(model.cur_sheet) if model.cur_sheet else "0"
                _res['set_title'] = title_json.get(cur_sheet) or ""
            elif attr == 'create_time':
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'delete_time':
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'delete_rtx':
                _res[attr] = getattr(model, 'delete_rtx', "")
            elif attr == 'is_del':
                _res[attr] = model.is_del or False
        else:
            return _res

    def dtalk_list(self, params: dict):
        """
        get dtalk list by params
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
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_page_comm_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
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

        # <get data>
        res, total = self.dtalk_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # ================= 遍历数据 ==================
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

    def dtalk_delete(self, params: dict):
        """
        delete one dtalk data by params
        params is dict
        """
        # ====================== parameters check ======================
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
            if k not in self.req_delete_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)

        # ====================== data check ======================
        model = self.dtalk_bo.get_model_by_md5(md5=new_params.get('md5'))
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
        # <update data> 软删除
        try:
            model.is_del = True
            model.delete_rtx = rtx_id
            model.delete_time = get_now()
            self.dtalk_bo.merge_model(model)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {'md5': new_params.get('md5')}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def dtalk_deletes(self, params: dict):
        """
        delete many dtalk data by params
        params is dict
        """
        # ====================== parameters check ======================
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
            if k not in self.req_deletes_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:   # parameter is not allow null
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
        # << batch delete >>
        try:
            res = self.dtalk_bo.batch_delete_by_md5(params=new_params)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {'md5': new_params.get('md5')}).json()

        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def dtalk_detail(self, params: dict):
        """
        get the latest dtalk message detail information by md5
        :return: json data
        """
        # ================== parameters check && format ==================
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
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_detail_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>>>>
        model = self.dtalk_bo.get_model_by_md5(new_params.get('md5'))
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
            100, 'success', StatusMsgs.get(100), self._dtalk_model_to_dict(model, _type='detail')
        ).json()

    def dtalk_update(self, params: dict):
        """
        update dtalk information by md5, contain:
            - name 文件名称
            - title 消息标题
            - set_sheet 设置的sheet
        :return: json data
        """
        # ====================== parameters check and format ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_dtalk_update_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # >>>>>>>>>>> new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_dtalk_update_attrs and v:      # 不合法参数
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v and k in self.req_dtalk_update_need_attrs:       # value check, is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            if k == 'name':      # check name and length
                new_names = os.path.splitext(str(v))
                if new_names[-1] not in self.EXCEL_FORMAT:
                    return Status(
                        217, 'failure', u'文件格式只支持.xls、.xlsx', {}).json()
                if not check_length(v, 80):  # check: length
                    return Status(
                        213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'title' and v:
                if not check_length(v, 50):  # check: length
                    return Status(
                        213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'set_sheet':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s数据类型为LIST' % k, {}).json()
                v = ';'.join(v)
            elif k == 'column':
                if not isinstance(v, list):
                    return Status(
                        213, 'failure', u'请求参数%s数据类型为LIST' % k, {}).json()
                if len(v) < 2:
                    if not isinstance(v, list):
                        return Status(
                            213, 'failure', u'请求参数%s数据至少选择2列' % k, {}).json()
                v = v
            else:
                v = str(v)
            new_params[k] = v

        # ========= check data ==========
        model = self.dtalk_bo.get_model_by_md5(md5=new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                310, 'failure', StatusMsgs.get(310), {}).json()

        # update
        # <update file real name>
        if str(new_params.get('name')) != str(model.file_name):
            res = self._update_real_file_name(model, new_params.get('name'))
            if res:
                model.file_name = res.get('name')
                model.file_local_url = res.get('local_url')
                model.file_store_url = res.get('store_url')
        model.title = new_params.get('title')
        model.set_sheet = new_params.get('set_sheet')
        # sheet设置
        cur_sheet = str(new_params.get('cur_sheet'))
        model.cur_sheet = cur_sheet
        # sheet title
        title_json = json.loads(model.set_title) if model.set_title else {}
        title_json[cur_sheet] = new_params.get('title') or ""
        model.set_title = json.dumps(title_json)
        # sheet column
        set_column_json = json.loads(model.set_column)
        if new_params.get('column'):
            set_column_json[cur_sheet] = new_params.get('column')
            model.set_column = json.dumps(set_column_json)
        try:
            self.dtalk_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def dtalk_change_sheet(self, params: dict):
        """
        dtalk change sheet by sheet index
        params is dict
        设置中切换sheet展示的内容切换（动态切换）
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_change_sheet_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # -------------------------- check parameters --------------------------
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_change_sheet_attrs:    # illegal parameter
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # check value is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)

        model = self.dtalk_bo.get_model_by_md5(md5=new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()

        ######################### get data
        cur_sheet = str(new_params.get('sheet')) if new_params.get('sheet') else "0"
        # current sheet title set
        title_json = json.loads(model.set_title) if model.set_title else {}
        title = title_json.get(cur_sheet) if title_json else ""
        # current column title set
        all_column_json = json.loads(model.sheet_columns)
        _set_column_json = json.loads(model.set_column)
        # 默认选择第一列，dtalk—user-id
        column = [0] if not _set_column_json \
            else _set_column_json.get(cur_sheet) or [0]
        columns = all_column_json.get(cur_sheet) or [] if all_column_json \
            else []
        data = {
            'set_title': title,
            'set_select_column': column,
            'set_columns': columns,
            'md5': new_params.get('md5')
        }
        return Status(
            100, 'success', StatusMsgs.get(100), data
        ).json()

    def _dtalk_robot_model_to_dict(self, model, _type='list'):
        """
        dtalk robot model to dict
        params model: dtalk robot model object
        attrs from class define attrs
        return dict data
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.dtalk_robot_attrs:
            if not attr: continue
            if attr == 'id':
                _res[attr] = getattr(model, 'id', '')
            elif attr == 'rtx_id':
                _res[attr] = getattr(model, 'rtx_id', '')
            elif attr == 'name':
                _res[attr] = getattr(model, 'name', '')
            elif attr == 'md5_id':
                _res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'key':
                _res[attr] = getattr(model, 'key', '')
            elif attr == 'secret':
                _res[attr] = getattr(model, 'secret', '')
            elif attr == 'select':
                _res[attr] = True if model.select else False
            elif attr == 'description':
                _res[attr] = getattr(model, 'description', '')
            elif attr == 'create_time':
                _res['create_time'] = self._transfer_time(model.create_time)
            elif attr == 'delete_time':
                _res['delete_time'] = self._transfer_time(model.delete_time)
            elif attr == 'delete_rtx':
                _res[attr] = getattr(model, 'delete_rtx', '')
            elif attr == 'is_del':
                _res[attr] = model.is_del or False
        else:
            return _res

    def _qywx_robot_model_to_dict(self, model, _type='list'):
        """
        qywx robot model to dict
        params model: qywx robot model object
        attrs from class define attrs
        return dict data
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.qywx_robot_attrs:
            if not attr: continue
            if attr == 'id':
                _res[attr] = getattr(model, 'id', '')
            elif attr == 'rtx_id':
                _res[attr] = getattr(model, 'rtx_id', '')
            elif attr == 'name':
                _res[attr] = getattr(model, 'name', '')
            elif attr == 'md5_id':
                _res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'key':
                _res[attr] = getattr(model, 'key', '')
            elif attr == 'secret':
                _res[attr] = getattr(model, 'secret', '')
            elif attr == 'agent':
                _res[attr] = getattr(model, 'agent', '')
            elif attr == 'select':
                _res[attr] = True if model.select else False
            elif attr == 'description':
                _res[attr] = getattr(model, 'description', '')
            elif attr == 'create_time':
                _res['create_time'] = self._transfer_time(model.create_time)
            elif attr == 'delete_time':
                _res['delete_time'] = self._transfer_time(model.delete_time)
            elif attr == 'delete_rtx':
                _res[attr] = getattr(model, 'delete_rtx', '')
            elif attr == 'is_del':
                _res[attr] = model.is_del or False
        else:
            return _res

    def dtalk_robot_list(self, params: dict):
        """
        get dtalk robot list by params
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
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_page_comm_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if k == 'limit':
                v = int(v) if v else OFFICE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            else:
                v = str(v) if v else ''
            new_params[k] = v
        # **************** 管理员获取ALL数据 *****************
        # 特权账号
        rtx_id = new_params.get('rtx_id')
        if new_params.get('rtx_id') in auth_rtx_join([]):
            new_params.pop('rtx_id')
        # <get data>
        res, total = self.dtalk_robot_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # ////////////////// return data \\\\\\\\\\\\\\\\\\\\\
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._dtalk_robot_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                # 特殊权限与普通账号都显示个人设置的默认选择
                _res_dict['select'] = True if _res_dict['select'] and _res_dict['rtx_id'] == rtx_id \
                    else False
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def dtalk_robot_add(self, params: dict):
        """
        add new dtalk robot, information contain:
        name: 机器人名称
        key: robot-key
        secret: robot-secret
        description: 机器人描述
        select: 是否默认
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.dtalk_robot_add_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        #################### check parameters ====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.dtalk_robot_add_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in ['select']:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            # type check
            if k == 'select' and not isinstance(v, bool):
                return Status(
                    213, 'failure', u'请求参数%s为Boolean类型' % k, {}).json()
            new_params[k] = str(v) if k not in ['select'] else v

        # check: length
        for _key, _value in self.dtalk_robot_add_ck_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # check key and secret is or not repeat
        if new_params.get('key') and new_params.get('secret'):
            if self.dtalk_robot_bo.get_model_by_key_secret(
                    key=new_params.get('key'),
                    secret=new_params.get('secret'),
                    rtx_id=new_params.get('rtx_id')):
                return Status(
                    213, 'failure', 'KEY与SECRET已存在，请勿重复添加', {}).json()
        # select default
        if new_params.get('select'):
            self.dtalk_robot_bo.update_unselect_by_rtx(rtx_id=new_params.get('rtx_id'))
        # --------------------------------------- add model --------------------------------------
        # 添加try异常处理，防止数据库add失败
        try:
            new_model = self.dtalk_robot_bo.new_mode()
            new_model.rtx_id = new_params.get('rtx_id')
            new_model.name = new_params.get('name')
            md5_id = md5(new_params.get('rtx_id')+new_params.get('key')+new_params.get('secret')+get_now())
            new_model.md5_id = md5_id
            new_model.key = new_params.get('key')
            new_model.secret = new_params.get('secret')
            new_model.select = new_params.get('select') or False
            new_model.description = new_params.get('description')
            new_model.create_time = get_now()
            new_model.is_del = False
            new_model.delete_time = ''
            self.dtalk_robot_bo.add_model(new_model)
        except:
            return Status(
                320, 'failure', StatusMsgs.get(320), {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': md5_id}).json()

    def dtalk_robot_delete(self, params: dict):
        """
        delete one dtalk robot data by params
        params is dict
        """
        # ====================== parameters check ======================
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
            if k not in self.req_delete_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)

        # ====================== data check ======================
        model = self.dtalk_robot_bo.get_model_by_md5(md5=new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                311, 'failure', StatusMsgs.get(311), {}).json()
        try:
            # <update data>
            model.is_del = True
            model.delete_rtx = rtx_id
            model.delete_time = get_now()
            self.dtalk_robot_bo.merge_model(model)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def dtalk_robot_deletes(self, params: dict):
        """
        delete many dtalk robot data by params
        params is dict
        """
        # ====================== parameters check ======================
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
            if k not in self.req_deletes_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v: # parameter is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            if k == 'list': # check type
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
        # << batch delete >>
        try:
            res = self.dtalk_robot_bo.batch_delete_by_md5(params=new_params)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()

        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def dtalk_robot_detail(self, params: dict):
        """
        get dtalk robot detail information by md5 from dtalk_robot table
        :return: json data
        """
        # no parameters
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
        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_detail_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>
        model = self.dtalk_robot_bo.get_model_by_md5(new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), self._dtalk_robot_model_to_dict(model, _type='detail')
        ).json()

    def dtalk_robot_update(self, params: dict):
        """
        update dtalk robot information by md5, contain:
            - name 名称
            - key
            - secret
            - description 描述
            - select 选择
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_dtalk_robot_update_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        #################### check parameters ====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_dtalk_robot_update_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in ['select']:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            # check: type
            if k == 'select' and not isinstance(v, bool):
                return Status(
                    213, 'failure', u'请求参数%s为Boolean类型' % k, {}).json()
            new_params[k] = str(v) if k not in ['select'] else v

        # check: length
        for _key, _value in self.dtalk_robot_add_ck_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # ========= check data ???????????
        model = self.dtalk_robot_bo.get_model_by_md5(md5=new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                310, 'failure', StatusMsgs.get(310), {}).json()

        # select default
        if new_params.get('select'):
            self.dtalk_robot_bo.update_unselect_by_rtx(rtx_id=new_params.get('rtx_id'))
        # --------------------------------------- update model --------------------------------------
        try:
            model.name = new_params.get('name')
            model.key = new_params.get('key')
            model.secret = new_params.get('secret')
            model.description = new_params.get('description')
            model.select = new_params.get('select') or False
            self.dtalk_robot_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def dtalk_robot_select(self, params: dict) -> json:
        """
        set dtalk robot default select status by md5
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_dtalk_robot_select_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        #################### check parameters ====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_dtalk_robot_select_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k != 'select':
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            # check: type
            if k == 'select' and not isinstance(v, bool):
                return Status(
                    213, 'failure', u'请求参数%s为Boolean类型' % k, {}).json()
            new_params[k] = str(v) if k != 'select' else v

        # ========= check data
        model = self.dtalk_robot_bo.get_model_by_md5(md5=new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                310, 'failure', StatusMsgs.get(310), {}).json()
        # status
        if new_params.get('select') != model.select:
            return Status(
                310, 'failure', '数据状态不一致，请刷新再设置' or StatusMsgs.get(310), {}).json()

        # select set
        """
        设置选择分2种：
            >>>>> 1.数据为选择状态，直接全都设置非选择
            >>>>> 2.数据为非选择状态，先全部设置非选择状态，再把选择的数据设置为选择
        """
        self.dtalk_robot_bo.update_unselect_by_rtx(rtx_id=new_params.get('rtx_id'))
        # --------------------------------------- update model --------------------------------------
        if not new_params.get('select'):
            model.select = True
            self.dtalk_robot_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def dtalk_send_init(self, params: dict) -> json:
        """
        dtalk send message initialize data
        :return: json data
        """
        # <<<<<<<<<<<<<<<<<<<<< parameters check >>>>>>>>>>>>>>>>>>>>
        # > no
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_dtalk_send_init_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # > check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_dtalk_send_init_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # ------------------------ dtalk data ------------------------
        dtalk_model = self.dtalk_bo.get_model_by_md5(new_params.get('md5'))
        # no dtalk model
        if not dtalk_model:
            set_sheet_index = []
            sheet_names = []
        else:
            set_sheet_index = [str(i) for i in str(dtalk_model.set_sheet).split(';')] if dtalk_model.set_sheet else ['0']  # 默认index为0
            json_sheet_names = json.loads(dtalk_model.sheet_names)
            sheet_names = list()
            if json_sheet_names:
                for k, v in json_sheet_names.items():
                    sheet_names.append({'key': k, 'value': v})
        # ========================= dtalk robot data =========================
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 特权账号 + 数据账号
        if rtx_id in auth_rtx_join([]):
            robot_models = self.dtalk_robot_bo.get_model_by_rtx('')
        else:
            robot_models = self.dtalk_robot_bo.get_model_by_rtx(rtx_id)
        # dtalk robot model
        select_robot_index = ''
        robot_enums = []
        if robot_models:
            for r in robot_models:
                if r.select and r.rtx_id == rtx_id:
                    select_robot_index = r.key
                robot_enums.append({'key': r.key, 'value': r.name})

        """     return json data    """
        _result = {
            'sheet_index': set_sheet_index,
            'sheet_names': sheet_names,
            'robot_index': select_robot_index,
            'robot_enums': robot_enums
        }
        return Status(
            100, 'success', StatusMsgs.get(100), _result
        ).json()

    def _dtalk_get_excel_data(self, excel_file: str, sheet_index: int = 0, columns: list = []) -> json:
        """
        获取源数据，主要操作有2步:
            第一获取excel表格数据
            第二对数据进行格式化，形成key: value格式

        :excel_file 文件
        :sheet_index sheet索引
        :columns 索引sheet需要格式化的列索引
        """
        ret_data = list()
        excel_json_data = self.excel_lib.read(read_file=excel_file, sheet=sheet_index,
                            request_title=True, response_title=True)
        if excel_json_data.get('status_id') != 100:
            return ret_data

        titles = excel_json_data.get('data').get('header')
        for _d in excel_json_data.get('data').get('data'):
            if not _d: continue
            ######### dtalk user id 为模板默认第一列
            dtalk_user_id = _d[0]
            if not dtalk_user_id: continue
            _unit = dict()
            for col in columns:
                col = int(col)
                if col < 0: continue
                if not titles[col] and not _d[col]: continue    # 没有title也没有data，直接pass
                _unit[titles[col]] = _d[col] or "/"    # 无内容的部分暂时用/代替
            ret_data.append({'id': dtalk_user_id, 'data': _unit})
        return ret_data

    def __format_message_json(self, content: dict, title: str) -> dict:
        """
        格式化推送的信息，string -> json
        获取config是否添加额外的图片
        后续定制专门的markdown信息，待开发TODO
        DingTalk 消息格式：
            {
                "title": "2021-12绩效明细",
                "text": "#### 2021-11绩效明细  \n  - 个人存款绩效：278  \n  - 贷款绩效：278  \n  - 部门履职绩效：278  \n  - 合规履职绩效：278  \n  - 存款下降扣发：278  \n  - ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)"
            }
        支持markdown语法
        \n代表换行，建议\n前后分别加2个空格
        参考：https://developers.dingtalk.com/document/app/message-types-and-data-format

        名称          类型          是否必填          示例值          描述
        msgtype      String        是               markdown      消息类型，Markdown类型为：markdown。
                                                                  消息链接跳转，请参考消息链接说明。
        title        String        是               测试标题        首屏会话透出的展示内容。
        text         String        是               测试内容        markdown格式的消息，建议500字符以内。
        """
        title = title if title else '%s自动化提醒' % get_now()
        text = '### %s' % title
        if DTALK_ADD_IMAGE:
            text += '  \n  - ![](%s)' % DTALK_ADD_IMAGE
        for _k, _v in content.items():
            if not _k and not _v: continue
            # TODO 只有数值型才为空才设置0
            if not _v: _v = 0
            if isinstance(_v, float):
                _v = round(_v, 2)
            text += '  \n  - %s: %s' % (_k, _v)
        ding_msg = {
            "title": '%s    详情...' % title,
            "text": text,
        }
        return ding_msg

    def dtalk_send(self, params: dict):
        """
        main entry
        消息程序主入口，在运行之前需要完成数据采集与处理、配置修改2个部分。
        1.数据采集与修改
            数据需要按照在template目录下面模板文件进行数据采集，文件名称以及内容采用固定方式，统一使用文件模板。
            - DingTalk User ID源于钉钉管理后台
            - 采集其他消息数据
            - 以模板内容为准，形成消息数据
        2.配置
            修改项目配置目录下的config.yaml文件，需要修改ROBOT配置下的APPKEY、APPSECRET，
            具体DingTalk ROBOT的创建、配置请查看README.md文件
        完成1&&2内容之后，运行此文件，其他文件内容无须更改
        :return: json data

        design:
            +------------------------------------------------------+
            | 1.Initialize source data:                            |
            |   - bank staff information data from db              |
            |   - salary data from db or bank (.xls or .xlsx)      |
            +------------------------------------------------------+
                      |
                      v
            +------------------------------------------------------+
            | 2.modify config file at project root folder          |
            +------------------------------------------------------+
                      |
                      v
            +------------------------------------------------------+
            | 3.run the main.py script file to send messages       |
            +------------------------------------------------------+
        """
        # <<< no parameters >>>
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_dtalk_send_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # ====================check parameters ====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_dtalk_send_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:       # check value is not allow null
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            if k == 'sheet' and not isinstance(v, list):        # check sheet type
                return Status(
                    210, 'failure', u'请求参数%s为类型为List' % k, {}).json()
            new_params[k] = str(v) if k != 'sheet' else v

        """ dtalk check: get dtalk model from dtalk_message table """
        dtalk_model = self.dtalk_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not dtalk_model:
            return Status(
                302, 'failure', 'dtalk数据不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if dtalk_model and dtalk_model.is_del:
            return Status(
                302, 'failure', 'dtalk数据已删除' or StatusMsgs.get(302), {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([dtalk_model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        """ dtalk robot check: get dtalk robot model from dtalk_robot table """
        robot_model = self.dtalk_robot_bo.get_model_by_key_rtx(key=new_params.get('robot'), rtx=new_params.get('rtx_id'))
        if not robot_model:
            return Status(
                302, 'failure', 'robot数据不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if robot_model and robot_model.is_del:
            return Status(
                302, 'failure', 'robot数据已删除' or StatusMsgs.get(302), {}).json()
        # not key or not secret
        if not robot_model.key or not robot_model.secret:
            return Status(
                214, 'failure', "缺少key或者secret，请完善配置信息", {}).json()

        # <<<<<< check template file and refer parameters >>>>>
        dtalk_file = dtalk_model.file_local_url
        if not dtalk_file or not os.path.exists(dtalk_file) \
                or not os.path.isfile(dtalk_file):
            return Status(
                302, 'failure', '文件不存在，请删除重新上传' or StatusMsgs.get(226), {}).json()
        # -------------------------------- check end --------------------------------
        ####### dtalk api test to ping #######
        dtalk_api = DtalkLib(app_key=robot_model.key, app_secret=robot_model.secret)
        if not dtalk_api.is_avail():
            return Status(
                499, 'failure', 'DingAPI初始化失败，请检查KEY或SECRET是否配置正确' or StatusMsgs.get(499), {}).json()
        # =================================== start run, for循环 =====================================================
        set_columns_json = json.loads(dtalk_model.set_column) if dtalk_model.set_column else {}
        set_titles_json = json.loads(dtalk_model.set_title) if dtalk_model.set_title else {}
        _res_data = list()  # 采用list类型，记录每个sheet数据状态
        """
        元素为dict，格式：
        sheet：sheet_index，
        ok：True or False
        message：result message
        """
        n = 0  # 记录发送次数
        for sheet_index in new_params.get('sheet'):
            if not str(sheet_index): continue
            _d = dict()
            _d['sheet'] = str(sheet_index)
            """
            excel data:
            [{'id': dtalk_user_id, 'data': _unit}, {'id': dtalk_user_id, 'data': _unit}, ......]
            """
            excel_data = self._dtalk_get_excel_data(excel_file=dtalk_file, sheet_index=int(sheet_index),
                                                    columns=set_columns_json.get(str(sheet_index)))
            if not excel_data:
                _d['message'] = '文件第%sSheet无数据' % (int(sheet_index) + 1)
                _d['ok'] = False
                _res_data.append(_d)
                continue
                # TODO 做成空数据直接return，但是有的执行了，需要优化
                # return Status(
                #     302, 'failure', '文件第%sSheet无数据' % (int(sheet_index) + 1), {}).json()

            # DingTalk push message
            s_l = list()
            f_l = list()
            for d in excel_data:
                if not d: continue
                if d.get('id') in DTALK_CONTROL: continue   #### 添加发送控制，配置文件 ####
                dtalk_user_id = d.get('id')
                res = dtalk_api.robot2send(
                    self.__format_message_json(content=d.get('data'), title=set_titles_json.get(str(sheet_index))),
                    dtalk_user_id)
                s_l.append(dtalk_user_id) if res.get('status_id') == 100 \
                    else f_l.append(dtalk_user_id)
                if DTALK_INTERVAL > 0:
                    time.sleep(random.uniform(0.01, DTALK_INTERVAL))
                n += 1
            _d['message'] = "成功：%s，失败：%s" % (len(s_l), len(f_l))
            _d['ok'] = True
            _res_data.append(_d)
        dtalk_api.close()       # 关闭dtalk api
        # ================= update dtalk count and number =================
        dtalk_model.count = dtalk_model.count + 1
        dtalk_model.number = dtalk_model.number + n
        dtalk_model.robot = robot_model.md5_id
        self.dtalk_bo.merge_model(dtalk_model)
        # ================= return data message =================
        _ret_message = ''
        _ret_flag = True
        sheet_names_json = json.loads(dtalk_model.sheet_names) if dtalk_model.sheet_names else {}
        if sheet_names_json:
            for _d in _res_data:
                if not _d: continue
                if not _d.get('ok'): _ret_flag = False
                _ret_message += '【%s】：%s' % (sheet_names_json.get(str(_d.get('sheet'))) or "Sheet", _d.get('message'))
        else:
            for _d in _res_data:
                if not _d: continue
                if not _d.get('ok'): _ret_flag = False
                _ret_message += '【%s】：%s' % (str(_d.get('sheet')) or "Sheet", _d.get('message'))
        # if not _ret_flag:
        #     return Status(
        #         101, 'success', _ret_message, {}).json()
        return Status(
            100, 'success', _ret_message, {}).json()

    def dtalk_robot_ping(self, params: dict) -> dict:
        """
        dtalk robot test to ping
        :return: json data
        """
        # ==================== parameters check and format ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_dtalk_robot_ping_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_dtalk_robot_ping_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)

        # <<<<<<<<<<<<<<<<<<<<< get data >>>>>>>>>>>>>>>>>>>>>
        model = self.dtalk_robot_bo.get_model_by_md5(md5=new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        # not key or not secret
        if not model.key or not model.secret:
            return Status(
                214, 'failure', "缺少KEY或SECRET，请完善配置信息", {}).json()
        # <<<<<<<<<<<<<<<<<<<<< ping >>>>>>>>>>>>>>>>>>>>>
        # ping test
        # 初始化DtalkLib类
        dtalk_api = DtalkLib(app_key=model.key, app_secret=model.secret)
        if not dtalk_api.is_avail():
            return Status(
                499, 'failure', 'DingAPI初始化失败，请检查KEY或SECRET是否配置正确' or StatusMsgs.get(499), {}).json()
        # 关闭DtalkLib
        dtalk_api.close()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def qywx_robot_list(self, params: dict):
        """
        get qywx robot list by params
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
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_page_comm_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if k == 'limit':
                v = int(v) if v else OFFICE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            else:
                v = str(v) if v else ''
            new_params[k] = v
        # **************** 管理员获取ALL数据 *****************
        # 特权账号
        rtx_id = new_params.get('rtx_id')
        if new_params.get('rtx_id') in auth_rtx_join([]):
            new_params.pop('rtx_id')
        # <get data>
        res, total = self.qywx_robot_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # ////////////////// return data \\\\\\\\\\\\\\\\\\\\\
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._qywx_robot_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                # 特殊权限与普通账号都显示个人设置的默认选择
                _res_dict['select'] = True if _res_dict['select'] and _res_dict['rtx_id'] == rtx_id \
                    else False
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def qywx_robot_add(self, params: dict):
        """
        add new qywx robot, information contain:
        name: 机器人名称
        key: robot-key
        secret: robot-secret
        agent: agent-id
        description: 机器人描述
        select: 是否默认
        :return: json data
        """
        # >>>>>>>>> no parameters
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.qywx_robot_add_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        #################### check parameters ====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.qywx_robot_add_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in ['select']:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            # special check: bool
            if k == 'select' and not isinstance(v, bool):
                return Status(
                    213, 'failure', u'请求参数%s为Boolean类型' % k, {}).json()
            new_params[k] = str(v) if k not in ['select'] else v
        # check: length
        for _key, _value in self.qywx_robot_attrs_length_check.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # check key and secret is or not repeat
        if new_params.get('key') and new_params.get('secret') and new_params.get('agent'):
            if self.qywx_robot_bo.get_model_by_key_secret_agent(
                    key=new_params.get('key'),
                    secret=new_params.get('secret'),
                    agent=new_params.get('agent'),
                    rtx_id=new_params.get('rtx_id')):
                return Status(
                    213, 'failure', '机器人已存在，请勿重复添加', {}).json()
        # select default
        if new_params.get('select'):
            self.qywx_robot_bo.update_unselect_by_rtx(rtx_id=new_params.get('rtx_id'))
        # --------------------------------------- add model --------------------------------------
        new_model = self.qywx_robot_bo.new_mode()
        new_model.rtx_id = new_params.get('rtx_id')
        new_model.name = new_params.get('name')
        md5_id = md5(new_params.get('rtx_id')+new_params.get('agent')+new_params.get('key')+new_params.get('secret')+get_now())
        new_model.md5_id = md5_id
        new_model.key = new_params.get('key')
        new_model.secret = new_params.get('secret')
        new_model.agent = new_params.get('agent')
        new_model.select = new_params.get('select') or False
        new_model.description = new_params.get('description')
        new_model.create_time = get_now()
        new_model.is_del = False
        new_model.delete_time = ''
        # 添加try异常处理，防止数据库add失败
        try:
            self.qywx_robot_bo.add_model(new_model)
            return Status(
                100, 'success', StatusMsgs.get(100), {'md5': md5_id}).json()
        except:
            return Status(
                450, 'failure', StatusMsgs.get(450), {'md5': md5_id}).json()

    def qywx_robot_delete(self, params: dict):
        """
        delete one qywx robot data by params
        params is dict
        """
        # ====================== parameters check ======================
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
            # check: not allow parameters
            if k not in self.req_delete_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)

        # ====================== data check ======================
        model = self.qywx_robot_bo.get_model_by_md5(md5=new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                311, 'failure', StatusMsgs.get(311), {}).json()
        # <update data>
        try:
            model.is_del = True
            model.delete_rtx = rtx_id
            model.delete_time = get_now()
            self.qywx_robot_bo.merge_model(model)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def qywx_robot_deletes(self, params: dict):
        """
        delete many qywx robot data by params
        params is dict
        """
        # ====================== parameters check ======================
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
            if k not in self.req_deletes_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:   # parameter is not allow null
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
        # << batch delete >>
        try:
            res = self.qywx_robot_bo.batch_delete_by_md5(params=new_params)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()

        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def qywx_robot_detail(self, params: dict):
        """
        get qywx robot latest detail information by md5
        :return: json data
        """
        # no parameters
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
        # parameters check
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # illegal
            if k not in self.req_detail_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # not null value
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>
        model = self.qywx_robot_bo.get_model_by_md5(new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), self._qywx_robot_model_to_dict(model, _type='detail')
        ).json()

    def qywx_robot_update(self, params: dict):
        """
        update qywx robot information, contain:
            - name 名称
            - key
            - secret
            - description 描述
            - select 选择
        by md5
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_qywx_robot_update_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        #################### check parameters ====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_qywx_robot_update_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in ['select']:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            # special check: bool
            if k == 'select' and not isinstance(v, bool):
                return Status(
                    213, 'failure', u'请求参数%s为Boolean类型' % k, {}).json()
            new_params[k] = str(v) if k != 'select' else v
        # check: length
        for _key, _value in self.qywx_robot_attrs_length_check.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # ========= check data
        model = self.qywx_robot_bo.get_model_by_md5(md5=new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                310, 'failure', StatusMsgs.get(310), {}).json()
        # select default
        if new_params.get('select'):
            self.qywx_robot_bo.update_unselect_by_rtx(rtx_id=new_params.get('rtx_id'))
        # --------------------------------------- update model --------------------------------------
        try:
            model.name = new_params.get('name')
            model.key = new_params.get('key')
            model.secret = new_params.get('secret')
            model.agent = new_params.get('agent')
            model.description = new_params.get('description')
            model.select = new_params.get('select') or False
            self.qywx_robot_bo.merge_model(model)
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def qywx_robot_select(self, params: dict):
        """
        set qywx robot default select status by md5
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_qywx_robot_select_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        #################### check parameters ====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_qywx_robot_select_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in ['select']:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            if k == 'select' and not isinstance(v, bool):
                return Status(
                    213, 'failure', u'请求参数%s为Boolean类型' % k, {}).json()
            new_params[k] = str(v) if k not in ['select']\
                else v

        # ========= check data
        model = self.qywx_robot_bo.get_model_by_md5(md5=new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                310, 'failure', StatusMsgs.get(310), {}).json()
        # status
        if new_params.get('select') != model.select:
            return Status(
                310, 'failure', '数据状态不一致，请刷新再设置' or StatusMsgs.get(310), {}).json()

        # select set
        """
        设置选择分2种：
            1.数据为选择状态，直接全都设置非选择
            2.数据为非选择状态，先全部设置非选择状态，再把选择的数据设置为选择
        """
        self.qywx_robot_bo.update_unselect_by_rtx(rtx_id=new_params.get('rtx_id'))
        # --------------------------------------- update model --------------------------------------
        if not new_params.get('select'):
            model.select = True
            self.qywx_robot_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def qywx_robot_ping(self, params: dict) -> dict:
        """
        qywx robot test to ping
        :return: json data
        """
        # ==================== parameters check and format ====================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_qywx_robot_ping_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_qywx_robot_ping_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)

        # <<<<<<<<<<<<<<<<<<<<< get data >>>>>>>>>>>>>>>>>>>>>
        model = self.qywx_robot_bo.get_model_by_md5(md5=new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        # not key or not secret
        if not model.key \
                or not model.secret \
                or not model.agent:
            return Status(
                214, 'failure', "缺少KEY或SECRET，请完善配置信息", {}).json()

        # --------------------------------------- get token from 企业微信  --------------------------------------
        # ping test
        qywx_lib = QYWXLib(corp_id=model.key, secret=model.secret, agent_id=model.agent)
        if not qywx_lib.check_token():
            return Status(
                499, 'failure', 'PING失败，请检查配置' or StatusMsgs.get(499), {}).json()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def __format_qywx_content(self, f_type, q_type, q_content):
        """
        format qywx message  content
        f_type: format type
        q_type: qywx message type
        q_content: qywx message content
        """
        if f_type == 'list':
            if q_type in self.temp_upload_types:
                try:
                    json_content = json.loads(q_content)
                    _file_name = json_content.get('name')
                    return _file_name \
                        if _file_name and len(_file_name) < AUTH_NUM \
                        else '%s...查看详情' % str(_file_name)[:AUTH_NUM - 1]
                except:
                    pass

            return q_content \
                if q_content and len(q_content) < AUTH_NUM \
                else '%s...查看详情' % str(q_content)[:AUTH_NUM - 1]
        else:
            return q_content

    def _qywx_model_to_dict(self, model, _type='list'):
        """
        qywx message model to dict
        params model: qywx model object
        attrs from class define attrs
        return dict data

        type is list table show data
        type is detail data detail and config
        """
        _res = dict()
        if not model:
            return _res

        for attr in self.qywx_list_attrs:
            if not attr: continue
            q_type = getattr(model, 'type', '')
            if attr == 'id':
                _res[attr] = getattr(model, 'id', '')
            elif attr == 'rtx_id':
                _res[attr] = getattr(model, 'rtx_id', '')
            elif attr == 'title':
                _res[attr] = getattr(model, 'title', '')
            elif attr == 'content':
                _res[attr] = self.__format_qywx_content(
                    f_type=_type, q_type=q_type,
                    q_content=getattr(model, 'content', ''))
            elif attr == 'user':
                _res[attr] = getattr(model, 'user', '')
            elif attr == 'md5_id':
                _res[attr] = getattr(model, 'md5_id', '')
            elif attr == 'msg_id':
                _res[attr] = getattr(model, 'msg_id', '')
            elif attr == 'robot':
                _res[attr] = getattr(model, 'robot', '')
            elif attr == 'type':
                _res[attr] = q_type
            elif attr == 'count':
                _res[attr] = getattr(model, 'count', 0)
            elif attr == 'enum_value':
                _res['type_name'] = getattr(model, 'enum_value', '')
            elif attr == 'last_send_time':
                _res['last_send_time'] = self._transfer_time(model.last_send_time)
            elif attr == 'create_time':
                _res['create_time'] = self._transfer_time(model.create_time)
            elif attr == 'delete_time':
                _res['delete_time'] = self._transfer_time(model.delete_time)
            elif attr == 'delete_rtx':
                _res[attr] = getattr(model, 'delete_rtx', '')
            elif attr == 'is_del':
                _res[attr] = model.is_del or False
            elif attr == 'is_back':
                _res[attr] = model.is_back or False
        else:
            return _res

    def qywx_list(self, params: dict):
        """
        get qywx message list from db table qywx_message by parameters
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
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_page_comm_attrs and v:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
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

        # <get data>
        new_params['enum_name'] = 'qywx-type'
        res, total = self.qywx_bo.get_all(new_params)
        if not res:
            return Status(
                101, 'failure', StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # ================= 遍历数据 ==================
        new_res = list()
        n = 1
        for _d in res:
            if not _d: continue
            _res_dict = self._qywx_model_to_dict(_d)
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, 'success', StatusMsgs.get(100), {'list': new_res, 'total': total}
        ).json()

    def qywx_delete(self, params: dict):
        """
        delete one qywx message data by params
        params is dict
        """
        # ====================== parameters check ======================
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
            if k not in self.req_delete_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = str(v)

        # ====================== data check ======================
        model = self.qywx_bo.get_model_by_md5(md5=new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                311, 'failure', StatusMsgs.get(311), {}).json()
        try:
            # <update data> 软删除
            model.is_del = True
            model.delete_rtx = rtx_id
            model.delete_time = get_now()
            self.qywx_bo.merge_model(model)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()

        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def qywx_deletes(self, params: dict):
        """
        delete many qywx message data by params
        params is dict
        """
        # ====================== parameters check ======================
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
            if k not in self.req_deletes_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:   # parameter is not allow null
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
        # << batch delete >>
        try:
            res = self.qywx_bo.batch_delete_by_md5(params=new_params)
        except:
            return Status(
                321, 'failure', StatusMsgs.get(321), {}).json()

        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def qywx_detail(self, params: dict):
        """
        get the latest qywx message detail information by md5
        :return: json data
        """
        # ================== parameters check && format ==================
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
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_detail_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>>>>
        model = self.qywx_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                302, 'failure', '数据已删除' or StatusMsgs.get(302), {}).json()

        """ ************ return data ************ """
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        """  return data """
        # enum: qywx-type
        enums = self.enum_bo.get_model_by_name('qywx-type')
        type_res = list()
        for e in enums:
            if not e: continue
            type_res.append({'label': str(e.value), 'value': str(e.key)})

        # >>>>>> robot列表
        # 特权账号 + 数据账号
        if rtx_id in auth_rtx_join([]):
            robots = self.qywx_robot_bo.get_model_by_rtx(rtx='')
        else:
            robots = self.qywx_robot_bo.get_model_by_rtx(rtx=rtx_id)
        robot_res = list()
        for r in robots:
            if not r: continue
            robot_res.append({'label': str(r.name), 'value': str(r.md5_id), 'rtx': str(r.rtx_id)})

        model_dict = self._qywx_model_to_dict(model, _type='detail')
        _res = {
            'title': model_dict.get('title'),
            'content': model_dict.get('content'),
            'user': model_dict.get('user'),
            'type': model_dict.get('type'),
            'type_lists': type_res,
            'robot': model_dict.get('robot'),
            'robot_lists': robot_res
        }
        return Status(
            100, 'success', StatusMsgs.get(100), _res).json()

    def qywx_update(self, params: dict):
        """
        update qywx message information, contain:
            - title 消息标题
            - content 消息内容
            - type 消息类型
            - user 用户列表
            - robot 机器人
        by data md5
        :return: json data
        """
        # ====================== parameters check and format ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_qywx_update_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_qywx_update_attrs and v:      # 不合法参数
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
            # check: length
        for _key, _value in self.req_qywx_add_length_check.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # <<<<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>>>>
        model = self.qywx_bo.get_model_by_md5(new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()

        # --------------------------------------- update model --------------------------------------
        try:
            model.title = new_params.get('title')
            model.content = new_params.get('content')
            model.type = new_params.get('type')
            model.user = new_params.get('user')
            model.robot = new_params.get('robot')
            self.qywx_bo.merge_model(model)
            return Status(
                100, 'success', StatusMsgs.get(100), {'md5': model.md5_id}).json()
        except:
            return Status(
                322, 'failure', StatusMsgs.get(322), {'md5': model.md5_id}).json()

    def qywx_add(self, params: dict) -> json:
        """
        add new qywx message data, information content: title, content, type
        :return: many json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_qywx_add_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        #################### check parameters ====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_qywx_add_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # check: length
        for _key, _value in self.req_qywx_add_length_check.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # 判断robot是否存在
        robot = new_params.get('robot')
        robot_model = self.qywx_robot_bo.get_model_by_md5(md5=robot)
        if not robot_model:
            return Status(
                213, 'failure', u'机器人不存在，请重新选择', {}).json()

        # --------------------------------------- add model --------------------------------------
        new_model = self.qywx_bo.new_mode()
        new_model.rtx_id = new_params.get('rtx_id')
        new_model.title = new_params.get('title')
        new_model.content = new_params.get('content')
        new_model.user = new_params.get('user')
        new_model.type = new_params.get('type')
        new_model.count = 0     # 默认发送次数为0
        md5_id = md5(new_params.get('rtx_id') + new_params.get('title') + new_params.get('content') + get_now())
        new_model.md5_id = md5_id
        """
        # 默认的robot，存储robot md5-id
        # default_robot_model = self.qywx_robot_bo.get_default_by_rtx(new_params.get('rtx_id'))
        # new_model.robot = getattr(default_robot_model, 'md5_id', '')    # 获取默认的robot
        """
        # 修改为form表单主动传入
        new_model.robot = robot
        new_model.create_time = get_now()
        new_model.is_del = False
        new_model.is_back = False
        new_model.delete_time = ''
        new_model.last_send_time = ''
        # 添加try异常处理，防止数据库add失败
        try:
            self.qywx_bo.add_model(new_model)
            return Status(
                100, 'success', StatusMsgs.get(100), {'md5': md5_id}).json()
        except:
            return Status(
                320, 'failure', StatusMsgs.get(320), {'md5': md5_id}).json()

    def qywx_add_init(self, params: dict) -> json:
        """
        新增企业微信消息记录初始化dialog枚举数据
        :return: many json data

        > 企业消息类型
        > 机器人列表
        """
        # parameters
        rtx_id = params.get('rtx_id')
        if not rtx_id:
            return Status(
                212, 'failure', u'缺少请求参数rtx' or StatusMsgs.get(212), {}).json()

        """   return data   """
        # >>>>>> 企业微信类型
        enums = self.enum_bo.get_model_by_name('qywx-type')
        type_res = list()
        for e in enums:
            if not e: continue
            type_res.append({'label': str(e.value), 'value': str(e.key)})
        # >>>>>> robot列表
        # 特权账号 + 数据账号
        if rtx_id in auth_rtx_join([]):
            robots = self.qywx_robot_bo.get_model_by_rtx(rtx='')
        else:
            robots = self.qywx_robot_bo.get_model_by_rtx(rtx=rtx_id)
        robot_res = list()
        # 当前用户选择的默认选择人
        select_robot = ''
        for r in robots:
            if not r: continue
            robot_res.append({'label': str(r.name), 'value': str(r.md5_id), 'rtx': str(r.rtx_id)})
            # 默认设置 && 并且是与当前rtx一致
            if r.select and rtx_id == r.rtx_id:
                select_robot = str(r.md5_id)
        # 临时消息发送获取当前用户默认选择robot
        _res = {
            'type_lists': type_res,
            'robot': select_robot,
            'robot_lists': robot_res
        }
        return Status(
            100, 'success', StatusMsgs.get(100), _res
        ).json()

    def qywx_send_init(self, params: dict):
        """
        发送企业微信消息记录初始化数据
        :return: json data
        """
        # ================== parameters check && format ==================
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
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_detail_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>>>>
        model = self.qywx_bo.get_model_by_md5(new_params.get('md5'))
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
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        """  return data """
        # return data: enum list
        enums = self.enum_bo.get_model_by_name('qywx-type')
        type_res = list()
        for e in enums:
            if not e: continue
            type_res.append({'label': str(e.value), 'value': str(e.key)})
        # return data: robot list
        # authority【管理员具有所有数据权限】所有robots
        # 特权账号 + 数据账号
        if rtx_id in auth_rtx_join([]):
            robots = self.qywx_robot_bo.get_model_by_rtx(rtx='')
        else:
            robots = self.qywx_robot_bo.get_model_by_rtx(rtx=rtx_id)
        robot_res = list()
        for r in robots:
            if not r: continue
            robot_res.append({'label': str(r.name), 'value': str(r.md5_id), 'rtx': str(r.rtx_id)})

        _res = {
            'title': getattr(model, 'title', ''),
            'content': getattr(model, 'content', ''),
            'user': getattr(model, 'user', ''),
            'type': getattr(model, 'type', ''),     # 选择的类型
            'type_lists': type_res,                 # 类型枚举
            'robot': getattr(model, 'robot', ''),   # 设置的机器人
            'robot_lists': robot_res                # 机器人枚举
        }
        return Status(
            100, 'success', StatusMsgs.get(100), _res).json()

    def qywx_send(self, params: dict):
        """
        qywx send message to user list
        发送企业微信消息
        :return: json data

        包含：正常发送功能、临时发送功能
        """
        # ====================== parameters check and format ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        # **********************************************************************
        # temp参数默认值，如果无temp参数默认为False，否则传入为True
        temp = params.get('temp') or False
        if not isinstance(temp, bool):
            return Status(
                213, 'failure', u'temp参数支持BOOLEAN类型', {}).json()
        if 'temp' in params.keys():
            params.pop('temp')
        # temp为True，无需md5参数；为False，必须md5参数
        # **********************************************************************

        # **************************************************************************
        """inspect api request necessary parameters"""
        _necessary_attrs = self.req_qywx_send_attrs
        # 如果是临时通知，检查attrs去掉md5参数
        if temp:
            _necessary_attrs.remove('md5')
        for _attr in _necessary_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_qywx_send_attrs and v:      # 不合法参数
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in self.req_qywx_send_temp_send_attrs:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            if k == 'user':     # user参数特殊性检查，不允许中文；分号
                if str(v).find('；') > -1:
                    return Status(
                        213, 'failure', u'请求参数%s分号为英文' % k, {}).json()
            new_params[k] = str(v)
        # check: length
        for _key, _value in self.req_qywx_add_length_check.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')

        # <<<<<<<<<<<<<<<<< qyex_meesgae model >>>>>>>>>>>>>>>>>>>>
        # 非临时消息
        if not temp:
            if not new_params.get('md5'):
                return Status(
                    213, 'failure', u'缺少md5参数', {}).json()
            # model校验是否可用数据
            model = self.qywx_bo.get_model_by_md5(new_params.get('md5'))
            # not exist
            if not model:
                return Status(
                    302, 'failure', '数据不存在' or StatusMsgs.get(302), {}).json()
            # deleted
            if model and model.is_del:
                return Status(
                    302, 'failure', '数据已删除' or StatusMsgs.get(302), {}).json()
            # 特权账号 + 数据账号
            if rtx_id not in auth_rtx_join([model.rtx_id]):
                return Status(
                    309, 'failure', StatusMsgs.get(309), {}).json()
        # <<<<<<<<<<<<<<<<< qyex_meesgae robot model >>>>>>>>>>>>>>>>>>>>
        # robot【传入参数】
        robot = new_params.get('robot')
        robot_model = self.qywx_robot_bo.get_model_by_md5(robot)
        if not robot_model:
            return Status(
                302, 'failure', '机器人配置不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if robot_model.is_del:
            return Status(
                302, 'failure', 'robot数据已删除' or StatusMsgs.get(302), {}).json()
        # not key or not secret or not agent
        if not robot_model.key \
                or not robot_model.secret \
                or not robot_model.agent:
            return Status(
                214, 'failure', "请完善机器人配置信息", {}).json()
        # --------------------------------------- send --------------------------------------
        qywx_lib = QYWXLib(corp_id=robot_model.key, secret=robot_model.secret, agent_id=robot_model.agent)
        if not qywx_lib.check_token():
            return Status(
                480, 'failure', '企业微信机器人token初始化失败' or StatusMsgs.get(499), {}).json()
        # <<<<<<<<<<<<<<<<< 消息内容 >>>>>>>>>>>>>>>>>>
        # user用户列表【传入参数】
        to_user = new_params.get('user').split(';')
        # 消息类型【传入参数】
        send_type = str(new_params.get('type'))
        if send_type not in qywx_lib.types:
            return Status(
                213, 'failure', '企业微信暂不支持此类型消息', {}).json()

        # if send_type in qywx_lib.temp_upload_types:
        #     # TODO 需要处理附件media_id与robot的权限
        #     pass
        try:
            # 消息内容【传入参数】
            new_content = dict()
            content = new_params.get('content')
            if send_type in ['text', 'markdown']:    # text, markdown消息
                new_content['data'] = content
                _q_res = qywx_lib.send(to_user=to_user, content=new_content, stype=send_type)
            elif send_type in qywx_lib.temp_upload_types:  # 'image voice video file
                json_content = json.loads(content)
                new_content['data'] = json_content.get('media_id')
                _q_res = qywx_lib.send(to_user=to_user, content=new_content, stype=send_type)
            else:
                return Status(
                    213, 'failure', '企业微信暂不支持此类型消息', {}).json()

            _q_res_json = json.loads(_q_res)
            if _q_res_json.get('status_id') != 100:
                return Status(
                    480, 'failure', '企业微信发送消息发送故障：%s' % _q_res_json.get('message'), {}).json()
        except Exception as e:
            return Status(
                499, 'failure', '企业微信发送消息发送故障：%s' % e, {}).json()
        try:
            # --------------------------------------- update model --------------------------------------
            # 非临时通知update
            if not temp:
                model.title = new_params.get('title')
                model.content = new_params.get('content')
                model.type = new_params.get('type')
                model.user = new_params.get('user')
                model.robot = new_params.get('robot')
                model.count = model.count + 1
                model.last_send_time = get_now()
                if _q_res_json \
                        and _q_res_json.get('data') \
                        and _q_res_json.get('data').get('msgid'):
                    model.msg_id = _q_res_json.get('data').get('msgid')
                self.qywx_bo.merge_model(model)
            else:
                # --------------------------------------- add model --------------------------------------
                new_model = self.qywx_bo.new_mode()     # 创建一个新的qyex_message模型
                new_model.rtx_id = new_params.get('rtx_id')
                new_model.delete_rtx = new_params.get('rtx_id')     # rtx_id = delete_rtx
                new_model.title = new_params.get('title')
                new_model.content = new_params.get('content')
                new_model.user = new_params.get('user')
                new_model.type = new_params.get('type')
                new_model.count = 0  # 默认发送次数为0
                md5_id = md5(new_params.get('rtx_id') + new_params.get('title') + new_params.get('content') + get_now())
                new_model.md5_id = md5_id
                """
                # 默认的robot，存储robot md5-id
                # default_robot_model = self.qywx_robot_bo.get_default_by_rtx(new_params.get('rtx_id'))
                # new_model.robot = getattr(default_robot_model, 'md5_id', '')    # 获取默认的robot
                """
                # 修改为form表单主动传入
                new_model.robot = new_params.get('robot')
                now_time = get_now()    # create_time = delete_time = last_send_time
                new_model.create_time = now_time
                new_model.delete_time = now_time
                new_model.last_send_time = now_time
                new_model.is_del = True     # 临时通知默认不显示
                new_model.is_back = False
                self.qywx_bo.add_model(new_model)
        except:
            return Status(
                450, 'failure', StatusMsgs.get(450), {'md5': model.md5_id}).json()
        return Status(
            100, 'success', '成功', {}).json()

    def qywx_send_init_temp(self, params: dict):
        """
        发送企业微信消息记录初始化数据
        【临时】
        :return: json data
        """

        # ================== parameters check && format ==================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_send_temp_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_send_temp_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)
        # <<<<<<<<<<<<<<<<< return data >>>>>>>>>>>>>>>>>>>>
        # qywx type
        enums = self.enum_bo.get_model_by_name('qywx-type')
        type_res = list()
        for e in enums:
            if not e: continue
            type_res.append({'label': str(e.value), 'value': str(e.key)})

        # >>>>>> robot列表
        # 特权账号 + 数据账号
        rtx_id = new_params.get('rtx_id')
        if rtx_id in auth_rtx_join([]):
            robots = self.qywx_robot_bo.get_model_by_rtx(rtx='')
        else:
            robots = self.qywx_robot_bo.get_model_by_rtx(rtx=rtx_id)
        robot_res = list()
        # 当前用户选择的默认选择人
        select_robot = ''
        for r in robots:
            if not r: continue
            robot_res.append({'label': str(r.name), 'value': str(r.md5_id), 'rtx': str(r.rtx_id)})
            # 默认设置 && 并且是与当前rtx一致
            if r.select and rtx_id == r.rtx_id:
                select_robot = str(r.md5_id)

        # 临时消息发送获取当前用户默认选择robot
        _res = {
            'type_lists': type_res,
            'robot': select_robot,    # 禁用默认选择机器人
            'robot_lists': robot_res
        }
        return Status(
            100, 'success', StatusMsgs.get(100), _res).json()

    def qywx_send_temp(self, params: dict):
        """
        qywx send message to user list
        发送企业微信消息【临时】
        :return: json data

        【废弃，与qywx_send结合】
        """
        # ====================== parameters check and format ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_qywx_send_temp_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_qywx_send_temp_attrs and v:      # 不合法参数
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            if k == 'user':     # user参数特殊性检查，不允许中文；分号
                if str(v).find('；') > -1:
                    return Status(
                        213, 'failure', u'请求参数%s分号为英文' % k, {}).json()
            new_params[k] = str(v)
        # check: length
        for _key, _value in self.req_qywx_add_length_check.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()

        # <<<<<<<<<<<<<<<<< qyex_meesgae robot model >>>>>>>>>>>>>>>>>>>>
        robot_model = self.qywx_robot_bo.get_model_by_md5(new_params.get('robot'))
        if not robot_model:
            return Status(
                302, 'failure', '机器人配置不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if robot_model.is_del:
            return Status(
                302, 'failure', 'robot数据已删除' or StatusMsgs.get(302), {}).json()
        # not key or not secret or not agent
        if not robot_model.key \
                or not robot_model.secret \
                or not robot_model.agent:
            return Status(
                214, 'failure', "请完善机器人配置信息", {}).json()
        # --------------------------------------- send --------------------------------------
        qywx_lib = QYWXLib(corp_id=robot_model.key, secret=robot_model.secret, agent_id=robot_model.agent)
        if not qywx_lib.check_token():
            return Status(
                480, 'failure', '企业微信机器人token初始化失败' or StatusMsgs.get(499), {}).json()
        try:
            # user用户列表
            to_user = new_params.get('user').split(';')
            # 消息类型
            send_type = str(new_params.get('type'))
            if send_type not in qywx_lib.types:
                return Status(
                    213, 'failure', '企业微信暂不支持此类型消息', {}).json()
            # 消息内容
            new_content = dict()
            if send_type in ['text', 'markdown']:  # text, markdown消息
                new_content['data'] = new_params.get('content')
                _q_res = qywx_lib.send(to_user=to_user, content=new_content, stype=send_type)
            else:
                return Status(
                    213, 'failure', '企业微信暂不支持此类型消息', {}).json()
            # <<<<<<<<<<<<<<<<< 临时发送不记录 >>>>>>>>>>>>>>>>>>>>
            _q_res_json = json.loads(_q_res)
            if _q_res_json.get('status_id') != 100:
                return Status(
                    480, 'failure', '企业微信发送消息发送故障：%s' % _q_res_json.get('message'), {}).json()
        except Exception as e:
            return Status(
                499, 'failure', '企业微信发送消息发送故障：%s' % e, {}).json()
        return Status(
            100, 'success', '成功', {}).json()

    def qywx_sendback(self, params: dict):
        """
        撤销最近24小时内发的企业微信消息
        :return: json data
        """
        # ====================== parameters check and format ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_qywx_backsend_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_qywx_backsend_attrs and v:      # 不合法参数
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)

        # <<<<<<<<<<<<<<<<< get model >>>>>>>>>>>>>>>>>>>>
        model = self.qywx_bo.get_model_by_md5(new_params.get('md5'))
        # not exist
        if not model:
            return Status(
                302, 'failure', '数据不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if model and model.is_del:
            return Status(
                302, 'failure', '数据已删除' or StatusMsgs.get(302), {}).json()
        # is not send
        if model and not model.msg_id:
            return Status(
                308, 'failure', '消息未发送，不允许撤销', {}).json()
        # not robot
        if model and not model.robot:
            return Status(
                308, 'failure', '消息未设置消息机器人，不允许撤销', {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([model.rtx_id]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()

        # <<<<<<<<<<<<<<<<< qyex_meesgae robot model >>>>>>>>>>>>>>>>>>>>
        robot_model = self.qywx_robot_bo.get_model_by_md5(model.robot)
        if not robot_model:
            return Status(
                302, 'failure', '机器人配置不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if robot_model.is_del:
            return Status(
                302, 'failure', 'robot数据已删除' or StatusMsgs.get(302), {}).json()
        # not key or not secret or not agent
        if not robot_model.key \
                or not robot_model.secret \
                or not robot_model.agent:
            return Status(
                214, 'failure', "请完善机器人配置信息", {}).json()
        # --------------------------------------- 撤销消息 --------------------------------------
        qywx_lib = QYWXLib(corp_id=robot_model.key, secret=robot_model.secret, agent_id=robot_model.agent)
        if not qywx_lib.check_token():
            return Status(
                480, 'failure', '企业微信机器人token初始化失败' or StatusMsgs.get(499), {}).json()
        try:
            _q_res = qywx_lib.sendback(message_id=model.msg_id)
            _q_res_json = json.loads(_q_res)
            if _q_res_json.get('status_id') != 100:
                return Status(
                    480, 'failure', '企业微信撤销消息故障：%s' % _q_res_json.get('message'), {}).json()
        except Exception as e:
            return Status(
                499, 'failure', '企业微信撤销消息故障：%s' % e, {}).json()
        # --------------------------------------- update model --------------------------------------
        try:
            model.is_back = True
            self.qywx_bo.merge_model(model)
        except:
            return Status(
                450, 'failure', StatusMsgs.get(450), {'md5': model.md5_id}).json()
        return Status(
            100, 'success', '成功', {}).json()

    def qywx_temp_upload(self, params, upload_file) -> dict:
        """
        企业微信上传临时素材
          > 素材上传得到media_id，该media_id仅三天内有效
          > media_id在同一企业内应用之间可以共享

        大小限制：
          > 图片（image）：10MB，支持JPG,PNG格式
          > 语音（voice） ：2MB，播放长度不超过60s，仅支持AMR格式
          > 视频（video） ：10MB，支持MP4格式
          > 普通文件（file）：20MB

        :return: json data

        相关URL：
          > 上传临时素材：https://developer.work.weixin.qq.com/document/path/90253
          > 上传图片：https://developer.work.weixin.qq.com/document/path/90256
        """
        # ====================== parameters check and format ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        if not upload_file:
            return Status(
                216, 'failure', StatusMsgs.get(216), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_qywx_temp_upload_attrs:
            if _attr not in params.keys():
                return Status(
                    212, 'failure', u'缺少请求参数%s' % _attr or StatusMsgs.get(212), {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_qywx_temp_upload_attrs and v:  # 不合法参数
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            new_params[k] = str(v)

        # <<<<<<<<<<<<<<<<< robot model >>>>>>>>>>>>>>>>>>>>
        robot = new_params.get('robot')
        robot_model = self.qywx_robot_bo.get_model_by_md5(robot)
        if not robot_model:
            return Status(
                302, 'failure', '机器人配置不存在' or StatusMsgs.get(302), {}).json()
        # deleted
        if robot_model.is_del:
            return Status(
                302, 'failure', 'robot数据已删除' or StatusMsgs.get(302), {}).json()
        # not key or not secret or not agent
        if not robot_model.key \
                or not robot_model.secret \
                or not robot_model.agent:
            return Status(
                214, 'failure', "请完善机器人配置信息", {}).json()
        # authority【管理员具有所有数据权限】
        rtx_id = new_params.get('rtx_id')
        # 特权账号 + 数据账号
        if rtx_id not in auth_rtx_join([getattr(robot_model, 'rtx_id')]):
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()

        upload_name = getattr(upload_file, 'filename')  # file public object

        # ======================= local store =======================
        # no file format filter
        # file local store
        is_ok, store_msg = self.file_lib.store_file(
            upload_file, compress=False, is_md5_store_name=False)
        if not is_ok:
            return Status(
                220, 'failure', StatusMsgs.get(220), {}).json()
        # get local file real store name
        if not upload_name:
            upload_name = os.path.split(store_msg.get('store_name'))[-1]
        # local file is or not real exist
        local_file = store_msg.get('path')
        if not os.path.exists(local_file) or not os.path.isfile(local_file):
            return Status(
                216, 'failure', StatusMsgs.get(216), {}).json()
        # ================================= store to tencent =================================
        qywx_lib = QYWXLib(corp_id=robot_model.key, secret=robot_model.secret, agent_id=robot_model.agent)
        if not qywx_lib.check_token():
            return Status(
                480, 'failure', '企业微信机器人token初始化失败' or StatusMsgs.get(499), {}).json()
        # upload type judge
        upload_type = new_params.get('type')
        if upload_type not in qywx_lib.temp_upload_types:
            return Status(
                213, 'failure', u'type消息类型不支持', {}).json()

        temp_upload_res = qywx_lib.temp_upload(upload_type=upload_type,
                                               upload_name=upload_name,
                                               upload_file=local_file)
        temp_upload_res_json = json.loads(temp_upload_res)
        # bad request
        if temp_upload_res_json.get('status_id') != 100:
            return temp_upload_res
        # return data
        data = {'name': upload_name}
        if temp_upload_res_json.get('data'):
            for k in ['type', 'media_id', 'created_at', 'url']:
                if temp_upload_res_json.get('data').get(k):
                    data[k] = temp_upload_res_json.get('data').get(k)
        return Status(
            100, 'success', '成功', data).json()


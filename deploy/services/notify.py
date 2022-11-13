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

from deploy.utils.excel_lib import ExcelLib
from deploy.utils.utils import get_now, d2s, check_length, md5
from deploy.bo.dtalk_message import DtalkMessageBo
from deploy.bo.dtalk_robot import DtalkRobotBo
from deploy.bo.qywx_message import QywxMessageBo
from deploy.bo.qywx_robot import QywxRobotBo
from deploy.bo.enum import EnumBo
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.config import OFFICE_LIMIT, SHEET_NUM_LIMIT, SHEET_NAME_LIMIT, \
    STORE_BASE_URL, STORE_SPACE_NAME, ADMIN, \
    DTALK_CONTROL, DTALK_INTERVAL, DTALK_TITLE, DTALK_ADD_IMAGE
from deploy.utils.store_lib import StoreLib
from deploy.utils.dtalk_lib import DtalkLib


class NotifyService(object):
    """
    notify service
    """

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
        'description',
        'select'
    ]

    qywx_robot_attrs_length_check = {
        'rtx_id': 25,
        'name': 30,
        'key': 30,
        'secret': 70,
        'description': 120
    }

    req_qywx_robot_update_attrs = [
        'rtx_id',
        'name',
        'key',
        'secret',
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
        'create_time',
        'delete_rtx',
        'delete_time',
        'is_del',
        'enum_name'
    ]

    req_qywx_add_attrs = [
        'rtx_id',
        'title',
        'content',
        'user',
        'type'
    ]

    req_qywx_add_length_check = {
        'title': 55,
        'content': 1000,
        'user': 1000
    }

    req_qywx_update_attrs = [
        'rtx_id',
        'title',
        'content',
        'user',
        'type',
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

    EXCEL_FORMAT = ['.xls', '.xlsx']

    DEFAULT_EXCEL_FORMAT = '.xlsx'

    def __init__(self):
        """
        notify service class initialize
        """
        super(NotifyService, self).__init__()
        self.excel_lib = ExcelLib()
        self.store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)
        self.dtalk_bo = DtalkMessageBo()
        self.dtalk_robot_bo = DtalkRobotBo()
        self.qywx_bo = QywxMessageBo()
        self.qywx_robot_bo = QywxRobotBo()
        self.enum_bo = EnumBo()

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
                _res[attr] = model.id
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id
            elif attr == 'file_name':
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
                    if len(set_sheet_name) > SHEET_NAME_LIMIT:  # 加了展示字数的限制，否则页面展示太多
                        set_sheet_name = '%s...具体查看请下载' % set_sheet_name[0:SHEET_NAME_LIMIT]
                    _res['set_sheet_name'] = set_sheet_name
                    _res['set_sheet_index'] = set_sheet_index
                else:
                    _res['sheet_names'] = []
                    _res['set_sheet_index'] = []
                    _res['set_sheet_name'] = ''
            elif attr == 'cur_sheet':
                _res[attr] = str(model.cur_sheet) if model.cur_sheet else "0"
            elif attr == 'set_column':
                _res[attr] = model.set_column if model.set_column else ""
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
                _res['create_time'] = d2s(model.create_time) if model.create_time else ''
            elif attr == 'delete_time':
                _res['delete_time'] = d2s(model.create_time) if model.create_time else ''
            elif attr == 'delete_rtx':
                _res[attr] = model.delete_rtx
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
        if new_params.get('rtx_id') == ADMIN:
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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                311, 'failure', StatusMsgs.get(311), {}).json()
        # <update data> 软删除
        model.is_del = True
        model.delete_rtx = rtx_id
        model.delete_time = get_now()
        self.dtalk_bo.merge_model(model)
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
        if new_params.get('rtx_id') == ADMIN:
            new_params.pop('rtx_id')
        # << batch delete >>
        res = self.dtalk_bo.batch_delete_by_md5(params=new_params)
        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def dtalk_detail(self, params: dict):
        """
        get the latest dtalk message detail information, by file md5
        :return: json data
        """
        # ================== parameters check && format ==================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        # return
        return Status(
            100, 'success', StatusMsgs.get(100), self._dtalk_model_to_dict(model, _type='detail')
        ).json()

    def dtalk_update(self, params: dict):
        """
        update dtalk information, contain:
            - name 文件名称
            - title 消息标题
            - set_sheet 设置的sheet
        by file md5
        :return: json data
        """
        # ====================== parameters check and format ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # new parameters
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

        # ========= check data
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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
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
        self.dtalk_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def dtalk_change_sheet(self, params: dict):
        """
        dtalk change sheet by sheet index
        params is dict
        设置中切换sheet展示的内容切换
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()

        # -------------------------- check parameters --------------------------
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_change_sheet_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            v = str(v)
            if not v:       # check value is not allow null
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}).json()
            new_params[k] = v

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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
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
                _res[attr] = model.id
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id
            elif attr == 'name':
                _res[attr] = model.name
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'key':
                _res[attr] = model.key
            elif attr == 'secret':
                _res[attr] = model.secret
            elif attr == 'select':
                _res[attr] = True if model.select else False
            elif attr == 'description':
                _res[attr] = model.description
            elif attr == 'create_time':
                _res['create_time'] = d2s(model.create_time) if model.create_time else ''
            elif attr == 'delete_time':
                _res['delete_time'] = d2s(model.create_time) if model.create_time else ''
            elif attr == 'delete_rtx':
                _res[attr] = model.delete_rtx
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
                _res[attr] = model.id
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id
            elif attr == 'name':
                _res[attr] = model.name
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'key':
                _res[attr] = model.key
            elif attr == 'secret':
                _res[attr] = model.secret
            elif attr == 'select':
                _res[attr] = True if model.select else False
            elif attr == 'description':
                _res[attr] = model.description
            elif attr == 'create_time':
                _res['create_time'] = d2s(model.create_time) if model.create_time else ''
            elif attr == 'delete_time':
                _res['delete_time'] = d2s(model.create_time) if model.create_time else ''
            elif attr == 'delete_rtx':
                _res[attr] = model.delete_rtx
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
        if new_params.get('rtx_id') == ADMIN:
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
            # check: length
            if k == 'rtx_id' and not check_length(v, 25):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'name' and not check_length(v, 30):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'key' and not check_length(v, 30):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'secret' and not check_length(v, 70):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'description' and not check_length(v, 120):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'select' and not isinstance(v, bool):
                return Status(
                    213, 'failure', u'请求参数%s为Boolean类型' % k, {}).json()
            new_params[k] = str(v) if k != 'select' else v

        # check key and secret is or not repeat
        if new_params.get('key') and new_params.get('secret'):
            if self.dtalk_robot_bo.get_model_by_key_secret(key=new_params.get('key'), secret=new_params.get('secret'), rtx_id=new_params.get('rtx_id')):
                return Status(
                    213, 'failure', 'KEY与SECRET已存在，请勿重复添加', {}).json()
        # select default
        if new_params.get('select'):
            self.dtalk_robot_bo.update_unselect_by_rtx(rtx_id=new_params.get('rtx_id'))
        # --------------------------------------- add model --------------------------------------
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
        # 添加try异常处理，防止数据库add失败
        try:
            self.dtalk_robot_bo.add_model(new_model)
            return Status(
                100, 'success', StatusMsgs.get(100), {'md5': md5_id}).json()
        except:
            return Status(
                450, 'failure', StatusMsgs.get(450), {'md5': md5_id}).json()

    def dtalk_robot_delete(self, params: dict):
        """
        delete one dtalk robot data by params
        params is dict
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                311, 'failure', StatusMsgs.get(311), {}).json()
        # <update data>
        model.is_del = True
        model.delete_rtx = rtx_id
        model.delete_time = get_now()
        self.dtalk_robot_bo.merge_model(model)
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
        if new_params.get('rtx_id') == ADMIN:
            new_params.pop('rtx_id')
        # << batch delete >>
        res = self.dtalk_robot_bo.batch_delete_by_md5(params=new_params)
        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def dtalk_robot_detail(self, params: dict):
        """
        get dtalk robot detail information, by file md5
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        # return data
        return Status(
            100, 'success', StatusMsgs.get(100), self._dtalk_robot_model_to_dict(model, _type='detail')
        ).json()

    def dtalk_robot_update(self, params: dict):
        """
        update dtalk robot information, contain:
            - name 名称
            - key
            - secret
            - description 描述
            - select 选择
        by file md5
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

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
            # check: length
            if k == 'rtx_id' and not check_length(v, 25):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'name' and not check_length(v, 30):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'key' and not check_length(v, 30):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'secret' and not check_length(v, 70):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'description' and not check_length(v, 120):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % k, {}).json()
            elif k == 'select' and not isinstance(v, bool):
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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                310, 'failure', StatusMsgs.get(310), {}).json()

        # select default
        if new_params.get('select'):
            self.dtalk_robot_bo.update_unselect_by_rtx(rtx_id=new_params.get('rtx_id'))
        # --------------------------------------- update model --------------------------------------
        model.name = new_params.get('name')
        model.key = new_params.get('key')
        model.secret = new_params.get('secret')
        model.description = new_params.get('description')
        model.select = new_params.get('select') or False
        self.dtalk_robot_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def dtalk_robot_select(self, params: dict):
        """
         set dtalk robot select status, by file md5
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
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
        self.dtalk_robot_bo.update_unselect_by_rtx(rtx_id=new_params.get('rtx_id'))
        # --------------------------------------- update model --------------------------------------
        if not new_params.get('select'):
            model.select = True
            self.dtalk_robot_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def dtalk_send_init(self, params: dict):
        """
        dtalk send message initialize data
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        # parameters check
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
        robot_model = self.dtalk_robot_bo.get_model_by_rtx(new_params.get('rtx_id'))
        if not robot_model:
            select_robot_index = ''
            robot_enums = []
        else:
            select_robot_index = ''
            robot_enums = []
            for r in robot_model:
                if r.select:
                    select_robot_index = r.key
                robot_enums.append({'key': r.key, 'value': r.name})
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
        # no parameters
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # ====================check parameters ====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_dtalk_send_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            if k == 'sheet' and not isinstance(v, list):
                return Status(
                    210, 'failure', u'请求参数%s为类型为List' % k, {}).json()
            new_params[k] = str(v) if k != 'sheet' else v

        """ dtalk check """
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
        if rtx_id != ADMIN and dtalk_model.rtx_id != rtx_id:
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        """ dtalk robot check """
        robot_model = self.dtalk_robot_bo.get_model_by_key_rtx(new_params.get('robot'), new_params.get('rtx_id'))
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

        # check template file and refer parameters
        dtalk_file = dtalk_model.file_local_url
        if not dtalk_file or not os.path.exists(dtalk_file) \
                or not os.path.isfile(dtalk_file):
            return Status(
                302, 'failure', '文件不存在，请删除重新上传' or StatusMsgs.get(226), {}).json()
        # -------------------------------- check end --------------------------------
        ####### dtalk api test to ping
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
                if d.get('id') in DTALK_CONTROL: continue   #### 添加发送控制，配置文件
                dtalk_user_id = d.get('id')
                res = dtalk_api.robot2send(
                    self.__format_message_json(content=d.get('data'), title=set_titles_json.get(str(sheet_index))),
                    dtalk_user_id)
                s_l.append(dtalk_user_id) if res.get('status_id') == 100 \
                    else f_l.append(dtalk_user_id)
                if DTALK_INTERVAL > 0:
                    time.sleep(random.uniform(0.1, DTALK_INTERVAL))
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
            new_params[k] = str(v) if k != 'select' else v

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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        # not key or not secret
        if not model.key or not model.secret:
            return Status(
                214, 'failure', "缺少KEY或SECRET，请完善配置信息", {}).json()
        # ping test
        dtalk_api = DtalkLib(app_key=model.key, app_secret=model.secret)
        if not dtalk_api.is_avail():
            return Status(
                499, 'failure', 'DingAPI初始化失败，请检查KEY或SECRET是否配置正确' or StatusMsgs.get(499), {}).json()
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
        if new_params.get('rtx_id') == ADMIN:
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
        description: 机器人描述
        select: 是否默认
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
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
            new_params[k] = str(v) if k != 'select' else v
        # check: length
        for _key, _value in self.qywx_robot_attrs_length_check.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    213, 'failure', u'请求参数%s长度超限制' % _key, {}).json()


        # check key and secret is or not repeat
        if new_params.get('key') and new_params.get('secret'):
            if self.qywx_robot_bo.get_model_by_key_secret(key=new_params.get('key'), secret=new_params.get('secret'), rtx_id=new_params.get('rtx_id')):
                return Status(
                    213, 'failure', 'KEY与SECRET已存在，请勿重复添加', {}).json()
        # select default
        if new_params.get('select'):
            self.qywx_robot_bo.update_unselect_by_rtx(rtx_id=new_params.get('rtx_id'))
        # --------------------------------------- add model --------------------------------------
        new_model = self.qywx_robot_bo.new_mode()
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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                311, 'failure', StatusMsgs.get(311), {}).json()
        # <update data>
        model.is_del = True
        model.delete_rtx = rtx_id
        model.delete_time = get_now()
        self.qywx_robot_bo.merge_model(model)
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
        if new_params.get('rtx_id') == ADMIN:
            new_params.pop('rtx_id')
        # << batch delete >>
        res = self.qywx_robot_bo.batch_delete_by_md5(params=new_params)
        return Status(100, 'success', StatusMsgs.get(100), {}).json() \
            if res == len(new_params.get('list')) \
            else Status(303, 'failure',
                        "结果：成功[%s]，失败[%s]" % (res, len(new_params.get('list'))-res) or StatusMsgs.get(303),
                        {'success': res, 'failure': (len(new_params.get('list'))-res)}).json()

    def qywx_robot_detail(self, params: dict):
        """
        get qywx robot detail information, by file md5
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                310, 'failure', StatusMsgs.get(310), {}).json()

        # select default
        if new_params.get('select'):
            self.qywx_robot_bo.update_unselect_by_rtx(rtx_id=new_params.get('rtx_id'))
        # --------------------------------------- update model --------------------------------------
        model.name = new_params.get('name')
        model.key = new_params.get('key')
        model.secret = new_params.get('secret')
        model.description = new_params.get('description')
        model.select = new_params.get('select') or False
        self.qywx_robot_bo.merge_model(model)
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def qywx_robot_select(self, params: dict):
        """
        set qywx robot select status by md5
        :return: json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

        #################### check parameters ====================
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_qywx_robot_select_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k != 'select':
                return Status(
                    214, 'failure', u'请求参数%s为必须信息' % k, {}).json()
            if k == 'select' and not isinstance(v, bool):
                return Status(
                    213, 'failure', u'请求参数%s为Boolean类型' % k, {}).json()
            new_params[k] = str(v) if k != 'select' else v

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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
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
            new_params[k] = str(v) if k != 'select' else v

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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        # not key or not secret
        if not model.key or not model.secret:
            return Status(
                214, 'failure', "缺少KEY或SECRET，请完善配置信息", {}).json()
        # TODO
        # ping test
        # dtalk_api = DtalkLib(app_key=model.key, app_secret=model.secret)
        # if not dtalk_api.is_avail():
        #     return Status(
        #         499, 'failure', 'DingAPI初始化失败，请检查KEY或SECRET是否配置正确' or StatusMsgs.get(499), {}).json()
        # dtalk_api.close()
        return Status(
            100, 'success', StatusMsgs.get(100), {'md5': new_params.get('md5')}
        ).json()

    def _qywx_model_to_dict(self, model):
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
            if attr == 'id':
                _res[attr] = model.id
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id
            elif attr == 'title':
                _res[attr] = model.title
            elif attr == 'content':
                _res[attr] = model.content
            elif attr == 'user':
                _res[attr] = model.user
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'robot':
                _res[attr] = model.robot
            elif attr == 'type':
                _res[attr] = model.type
            elif attr == 'enum_name':
                _res['type_name'] = model.enum_name
            elif attr == 'create_time':
                _res['create_time'] = d2s(model.create_time) if model.create_time else ''
            elif attr == 'delete_time':
                _res['delete_time'] = d2s(model.create_time) if model.create_time else ''
            elif attr == 'delete_rtx':
                _res[attr] = model.delete_rtx
            elif attr == 'is_del':
                _res[attr] = model.is_del or False
        else:
            return _res

    def qywx_list(self, params: dict):
        """
        get qywx message list by params, params is dict
        return json data
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()

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
        if new_params.get('rtx_id') == ADMIN:
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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                311, 'failure', StatusMsgs.get(311), {}).json()
        # <update data> 软删除
        model.is_del = True
        model.delete_rtx = rtx_id
        model.delete_time = get_now()
        self.qywx_bo.merge_model(model)
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
        if new_params.get('rtx_id') == ADMIN:
            new_params.pop('rtx_id')
        # << batch delete >>
        res = self.qywx_bo.batch_delete_by_md5(params=new_params)
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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        """  return data """
        # enum
        enums = self.enum_bo.get_model_by_name('qywx-type')
        type_res = list()
        for e in enums:
            if not e: continue
            type_res.append({'label': str(e.value), 'value': str(e.key)})
        _res = {
            'title': getattr(model, 'title', ''),
            'content': getattr(model, 'content', ''),
            'user': getattr(model, 'user', ''),
            'type': getattr(model, 'type', ''),
            'type_lists': type_res
        }
        return Status(
            100, 'success', StatusMsgs.get(100), _res).json()

    def qywx_update(self, params: dict):
        """
        update qywx message information, contain:
            - title 消息标题
            - content 消息内容
            - type 消息类型
        by data md5
        :return: json data
        """
        # ====================== parameters check and format ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()

        # --------------------------------------- update model --------------------------------------
        model.title = new_params.get('title')
        model.content = new_params.get('content')
        model.type = new_params.get('type')
        model.user = new_params.get('user')
        try:
            self.qywx_bo.merge_model(model)
            return Status(
                100, 'success', StatusMsgs.get(100), {'md5': model.md5_id}).json()
        except:
            return Status(
                450, 'failure', StatusMsgs.get(450), {'md5': model.md5_id}).json()

    def qywx_add(self, params: dict) -> json:
        """
        add new qywx message data, information content: title, content, type
        :return: many json data
        """
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
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

        default_robot_model = self.qywx_robot_bo.get_default_by_rtx(new_params.get('rtx_id'))
        # --------------------------------------- add model --------------------------------------
        new_model = self.qywx_bo.new_mode()
        new_model.rtx_id = new_params.get('rtx_id')
        new_model.title = new_params.get('title')
        new_model.content = new_params.get('content')
        new_model.user = new_params.get('user')
        new_model.type = new_params.get('type')
        md5_id = md5(new_params.get('rtx_id') + new_params.get('title') + new_params.get('content') + get_now())
        new_model.md5_id = md5_id
        new_model.robot = getattr(default_robot_model, 'md5_id', '')
        new_model.create_time = get_now()
        new_model.is_del = False
        new_model.delete_time = ''
        # 添加try异常处理，防止数据库add失败
        try:
            self.qywx_bo.add_model(new_model)
            return Status(
                100, 'success', StatusMsgs.get(100), {'md5': md5_id}).json()
        except:
            return Status(
                450, 'failure', StatusMsgs.get(450), {'md5': md5_id}).json()

    def qywx_add_init(self):
        """
        新增企业微信消息记录初始化dialog枚举数据
        :return: many json data
        """
        # no parameters
        enums = self.enum_bo.get_model_by_name('qywx-type')
        type_res = list()
        for e in enums:
            if not e: continue
            type_res.append({'label': str(e.value), 'value': str(e.key)})
        return Status(
            100, 'success', StatusMsgs.get(100), {'type': type_res}
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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()
        """  return data """
        # enum
        enums = self.enum_bo.get_model_by_name('qywx-type')
        type_res = list()
        for e in enums:
            if not e: continue
            type_res.append({'label': str(e.value), 'value': str(e.key)})
        # robot
        robots = self.qywx_robot_bo.get_model_by_rtx(rtx=rtx_id)
        robot_res = list()
        for r in robots:
            if not r: continue
            robot_res.append({'label': str(r.name), 'value': str(r.md5_id)})
        _res = {
            'title': getattr(model, 'title', ''),
            'content': getattr(model, 'content', ''),
            'user': getattr(model, 'user', ''),
            'type': getattr(model, 'type', ''),
            'type_lists': type_res,
            'robot': getattr(model, 'robot', ''),
            'robot_lists': robot_res
        }
        return Status(
            100, 'success', StatusMsgs.get(100), _res).json()

    def qywx_send(self, params: dict):
        """
        发送企业微信消息记录初始化数据
        :return: many json data
        """
        # ====================== parameters check and format ======================
        if not params:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}).json()
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_qywx_send_attrs and v:      # 不合法参数
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
        if rtx_id != ADMIN and model.rtx_id != rtx_id:
            return Status(
                309, 'failure', StatusMsgs.get(309), {}).json()

        # --------------------------------------- update model --------------------------------------
        model.title = new_params.get('title')
        model.content = new_params.get('content')
        model.type = new_params.get('type')
        model.user = new_params.get('user')
        model.robot = new_params.get('robot')
        try:
            self.qywx_bo.merge_model(model)
        except:
            return Status(
                450, 'failure', StatusMsgs.get(450), {'md5': model.md5_id}).json()

        # --------------------------------------- send --------------------------------------
        pass

# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    image service

base_info:
    __author__ = "PyGo"
    __time__ = "2023/7/20 23:23"
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
# usage: /usr/bin/python image.py
# ------------------------------------------------------------
import random

from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.utils import d2s, s2d, check_length, auth_rtx_join
from deploy.config import STORE_BASE_URL, STORE_SPACE_NAME, USER_DEFAULT_AVATAR
# bo
from deploy.bo.sysuser_avatar import SysUserAvatarBo
from deploy.bo.sysuser import SysUserBo
# lib
from deploy.delib.store_lib import StoreLib


class ImageService(object):
    """
    image service
    """

    PAGE_LIMIT = 15

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

    req_profile_avatar_set_attrs = [
        'rtx_id',
        'avatar',
    ]

    req_profile_avatar_set_ck_len_attrs = {
        'rtx_id': 25,
        'avatar': 120
    }

    sysuser_avatar_return_list_attrs = [
        # 'id',
        'name',
        'rtx_id',
        'md5_id',
        'type',
        'type_name',
        'summary',
        'label',
        'url',
        # 'or_url',
        'count',
        'create_time',
        'update_rtx',
        'update_time',
        # 'delete_rtx',
        # 'delete_time',
        # 'is_del',
        'order_id'
    ]

    sysuser_avatar_return_detail_attrs = [
        # 'id',
        'name',
        'rtx_id',
        'md5_id',
        'type',
        # 'type_name',
        'summary',
        'label',
        'url',
        'or_url',
        'count',
        'create_time',
        'update_rtx',
        'update_time',
        'delete_rtx',
        'delete_time',
        'is_del',
        'order_id'
    ]

    sysuser_avatar_return_profile_attrs = [
        'name',
        'md5_id',
        'type',
        'url',
        'or_url'
    ]

    def __init__(self):
        """
        ImageService class initialize
        """
        super(ImageService, self).__init__()
        # bo
        self.sysuser_avatar_bo = SysUserAvatarBo()
        self.sysuser_bo = SysUserBo()
        # lib
        self.store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)

    def __str__(self):
        print("ImageService class.")

    def __repr__(self):
        self.__str__()

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

    def _sysuser_avatar_model_to_dict(self, model, _type='list'):
        """
        enum model transfer to dict data
        """
        _res = dict()
        if not model:
            return _res

        if _type == 'list':
            attrs = self.sysuser_avatar_return_list_attrs
        elif _type == 'avatar':
            attrs = self.sysuser_avatar_return_profile_attrs
        elif _type == 'detail':
            attrs = self.sysuser_avatar_return_detail_attrs
        else:
            return _res

        for attr in attrs:
            if not attr: continue
            if attr == 'id':
                _res[attr] = model.id
            elif attr == 'name':
                _res[attr] = model.name
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id
            elif attr == 'type':
                _res[attr] = model.type
            elif attr == 'type_name':
                _res[attr] = model.type_name
            elif attr == 'summary':
                _res[attr] = model.summary
            elif attr == 'label':
                # 图片标签，以英文;分隔
                labels = str(model.label).split(';') if model.label else []
                if not labels:
                    _res[attr] = labels
                else:
                    new_labels = []
                    for l in labels:
                        if not l: continue
                        _new_label = {'type': l, 'index': random.randint(0, 3)}
                        new_labels.append(_new_label)
                    _res[attr] = new_labels
            elif attr == 'url':
                _res[attr] = self.store_lib.open_download_url(store_name=model.url) \
                    if model.url else ''
            elif attr == 'or_url':
                _res[attr] = self.store_lib.open_download_url(store_name=model.or_url) \
                    if model.or_url else ''
            elif attr == 'count':
                _res[attr] = model.count or 0
            elif attr == 'create_time':
                _res[attr] = self._transfer_time(model.create_time)
            elif attr == 'update_rtx':
                _res[attr] = model.update_rtx
            elif attr == 'update_time':
                _res[attr] = self._transfer_time(model.update_time)
            elif attr == 'delete_rtx':
                _res[attr] = model.delete_rtx
            elif attr == 'delete_time':
                _res[attr] = self._transfer_time(model.delete_time)
            elif attr == 'is_del':
                _res[attr] = model.is_del or False
            elif attr == 'order_id':
                _res[attr] = model.order_id or 1
        else:
            return _res

    def profile_avatar_list(self, params: dict) -> dict:
        """
        get profile avatar data list by params
        params is dict
        return json data
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                400, StatusEnum.FAILURE.value, StatusMsgs.get(400), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_page_comm_attrs:
            if _attr not in params.keys():
                return Status(
                    400, StatusEnum.FAILURE.value, '缺少请求参数%s' % _attr, {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            if k not in self.req_page_comm_attrs:
                return Status(
                    401, StatusEnum.FAILURE.value, '请求参数%s不合法' % k, {}).json()
            if k == 'limit':
                v = int(v) if v else self.PAGE_LIMIT
            elif k == 'offset':
                v = int(v) if v else 0
            else:
                v = str(v) if v else ''
            new_params[k] = v

        # **************** <get data> *****************
        rtx_id = new_params.get('rtx_id')
        # 全量
        new_params.pop('rtx_id')
        res, total = self.sysuser_avatar_bo.get_all(params=new_params, enum_name='avatar-type')
        # no data
        if not res:
            return Status(
                101, StatusEnum.SUCCESS.value, StatusMsgs.get(101), {'list': [], 'total': 0}).json()
        # <<<<<<<<<<<<<<<<<<<< format and return data >>>>>>>>>>>>>>>>>>>>
        new_res = list()
        n = 1 + new_params.get('offset')
        for _d in res:
            if not _d: continue
            _res_dict = self._sysuser_avatar_model_to_dict(_d, _type='avatar')
            if _res_dict:
                _res_dict['id'] = n
                new_res.append(_res_dict)
                n += 1
        return Status(
            100, StatusEnum.SUCCESS.value, StatusMsgs.get(100), {'list': new_res, 'total': total, 'rtx_id': rtx_id}
        ).json()

    def profile_avatar_set(self, params: dict) -> dict:
        """
        set profile avatar url list by params
        params is dict
        return json data
        """
        # ====================== parameters check ======================
        if not params:
            return Status(
                400, StatusEnum.FAILURE.value, StatusMsgs.get(400), {}).json()
        # **************************************************************************
        """inspect api request necessary parameters"""
        for _attr in self.req_profile_avatar_set_attrs:
            if _attr not in params.keys():
                return Status(
                    400, StatusEnum.FAILURE.value, '缺少请求参数%s' % _attr, {}).json()
        """end"""
        # **************************************************************************
        # new parameters
        new_params = dict()
        for k, v in params.items():
            if not k: continue
            # check: not allow parameters
            if k not in self.req_profile_avatar_set_attrs:
                return Status(
                    401, StatusEnum.FAILURE.value, '请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v:  # is not null
                return Status(
                    403, StatusEnum.FAILURE.value, '请求参数%s不允许为空' % k, {}).json()
            new_params[k] = v
        # parameters length check
        for _key, _value in self.req_profile_avatar_set_ck_len_attrs.items():
            if not _key: continue
            if not check_length(new_params.get(_key), _value):
                return Status(
                    405, StatusEnum.FAILURE.value, '请求参数%s长度超出限制' % _key, {}).json()

        # **************** <get avatar data> *****************
        avatar_model = self.sysuser_avatar_bo.get_model_by_md5(new_params.get('avatar'))
        # check
        if not avatar_model or not avatar_model.url:
            return Status(
                501, StatusEnum.FAILURE.value, "图片不存在，请重新选择", {}).json()

        # **************** <get sysuser data> *****************
        rtx_id = new_params.get('rtx_id')
        user_model = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        # check
        if not user_model:
            return Status(
                501, StatusEnum.FAILURE.value, '用户%s不存在' % rtx_id, {}).json()
        # authority【管理员具有所有数据权限】
        # 权限账户
        if rtx_id not in auth_rtx_join([user_model.rtx_id]):
            return Status(
                504, StatusEnum.FAILURE.value, "非数据权限人员，无权限操作", {}).json()

        # <<<<<<<<<<<<< update user avatar >>>>>>>>>>>>>
        try:
            # 第一步：设置用户头像
            avatar_url = self.store_lib.open_download_url(store_name=avatar_model.url) \
                    if avatar_model.url else USER_DEFAULT_AVATAR
            setattr(user_model, 'avatar', avatar_url)
            self.sysuser_bo.merge_model(user_model)

            # 第二步：更新图像设置数量
            avatar_model.count = avatar_model.count + 1
            self.sysuser_avatar_bo.merge_model(avatar_model)

            return Status(
                100, StatusEnum.SUCCESS.value, StatusMsgs.get(100), {'rtx_id': rtx_id, 'avatar': avatar_url}
            ).json()
        except:
            return Status(
                603, StatusEnum.FAILURE.value, "数据库更新数据失败", {'rtx_id': rtx_id}
            ).json()


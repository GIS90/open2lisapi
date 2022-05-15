# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    the services of sysuser

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "twtoolbox_isapi"

usage:

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.
------------------------------------------------
"""
from deploy.bo.sysuser import SysUserBo
from deploy.bo.menu import MenuBo
from deploy.services.menu import MenuService
from deploy.utils.utils import d2s, get_now
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.utils.logger import logger as LOG
from deploy.config import ADMIN, O_NOBN, STORE_SPACE_NAME, STORE_BASE_URL
from deploy.utils.store_lib import StoreLib
from deploy.utils.image_lib import ImageLib


class SysUserService(object):

    def __init__(self):
        """
        instance initialize
        """
        super(SysUserService, self).__init__()
        self.sysuser_bo = SysUserBo()
        self.menu_bo = MenuBo()
        self.menu_service = MenuService()
        self.store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)
        self.image_lib = ImageLib()
        self.base_attrs = ['id', 'rtx_id', 'md5_id', 'fullname', 'password',
                           'email', 'phone', 'avatar', 'introduction', 'department', 'role']
        self.extend_attrs = ['create_time', 'create_rtx', 'is_del', 'delete_time', 'delete_rtx']
        self.auth_attrs = ['authority', 'role_eng', 'role_chn']
        self.update_attrs = ['name', 'email', 'phone', 'avatar',
                             'introduction', 'department', 'role']
        self.password_attrs = ['old_password', 'new_password', 'con_password']

    def _model_to_dict(self, model, _type: str = 'base') -> dict:
        """
        db model transfer to dict data
        model: user model
        """
        if not model:
            return {}
        if _type == 'base':
            attrs = self.base_attrs
        elif _type == 'auth':
            attrs = self.base_attrs + self.auth_attrs
        elif _type == 'all':
            attrs = self.base_attrs + self.auth_attrs + self.extend_attrs
        else:
            attrs = self.base_attrs
        _res = dict()
        for attr in attrs:
            if attr == 'id':
                _res[attr] = model.id or ""
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id or ""
            elif attr == 'md5_id':
                _res[attr] = model.md5_id or ""
            elif attr == 'fullname':
                _res['name'] = model.fullname or ""
            elif attr == 'password':
                _res[attr] = model.password or ""
            elif attr == 'email':
                _res[attr] = model.email or ""
            elif attr == 'phone':
                _res[attr] = model.phone or ""
            elif attr == 'avatar':
                _res[attr] = model.avatar or ""
            elif attr == 'introduction':
                _res[attr] = model.introduction or ""
            elif attr == 'department':
                _res[attr] = model.department or ""
            elif attr == 'role':
                _res[attr] = model.role or ""
            elif attr == 'role_eng':
                _res[attr] = model.role_eng or ""
            elif attr == 'role_chn':
                _res[attr] = model.role_chn or ""
            elif attr == 'authority':
                _res[attr] = model.authority or ""
            elif attr == 'create_time':
                _res[attr] = d2s(model.create_time) \
                    if not isinstance(model.create_time, str) else model.create_time or ''
            elif attr == 'create_rtx':
                _res[attr] = model.create_rtx or ''
            elif attr == 'is_del':
                _res[attr] = True if model.is_del else False
            elif attr == 'delete_time':
                _res[attr] = d2s(model.delete_time) \
                    if not isinstance(model.delete_time, str) else model.delete_time or ''
            elif attr == 'delete_rtx':
                _res[attr] = model.delete_rtx or ""
        else:
            return _res

    def get_user_by_rtx_id(self, rtx_id: str) -> dict:
        """
        get user model by rtx id
        """
        user_res = dict()
        if not rtx_id:
            return user_res

        user = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        return self._model_to_dict(user, _type='base') if user else user_res

    def get_login_by_rtx(self, rtx_id: str) -> dict:
        """
        get login user by rtx id
        """
        user_res = dict()
        if not rtx_id:
            return user_res

        user = self.sysuser_bo.get_user_by_params(rtx_id)
        return self._model_to_dict(user, _type='base') if user else user_res

    def get_user_by_token(self, token: str, is_vue: bool = False) -> dict:
        """
        get user model by token
        """
        user_res = dict()
        if not token:
            return user_res

        user = self.sysuser_bo.get_user_by_token(token)
        return self._model_to_dict(user, _type='base') if user else user_res

    def get_login_by_token(self, token: str) -> dict:
        """
        get login user model by token
        token: user token
        """
        if not token:
            return Status(
                200, 'failure', StatusMsgs.get(200) or u'用户未登录', {}
            ).json()
        user_model = self.get_user_by_token(token, is_vue=True)
        if not user_model:
            return Status(
                302, 'failure', StatusMsgs.get(202) or u'用户未注册', {}
            ).json()
        if user_model.get('is_del'):
            return Status(
                302, 'failure', StatusMsgs.get(203) or u'用户已注销', {}
            ).json()

        LOG.info('%s login info rtx_id ==========' % user_model.get('rtx_id') or O_NOBN)
        if user_model.get('password'):
            del user_model['password']
        return Status(
            100, 'success', StatusMsgs.get(100),
            {'user': user_model, 'token': token} or {}
        ).json()

    def get_login_auth_by_rtx(self, rtx_id: str) -> dict:
        """
        get login auth model by rtx
        rtx_id: user rtx id
        """
        if not rtx_id:
            return Status(
                212, 'failure', u'缺少rtx_id请求参数', {}
            ).json()
        rtx_id = rtx_id.strip()  # 去空格
        user = self.sysuser_bo.get_auth_by_rtx(rtx_id)
        if not user:
            return Status(
                202, 'failure', StatusMsgs.get(202) or u'用户未注册', {}
            ).json()
        user_res = self._model_to_dict(user, _type='auth')
        if user_res.get('is_del'):
            return Status(
                203, 'failure', StatusMsgs.get(203) or u'用户已注销', {}
            ).json()

        auth_list = [int(x) for x in user_res.get('authority').split(';') if x]
        is_admin = True if user_res.get('rtx_id') == ADMIN \
            else False
        user_auth = self.menu_service.get_routes(auth_list, is_admin) or []
        LOG.info('%s login auth rtx_id ==========' % user_res.get('rtx_id') or O_NOBN)
        return Status(
            100, 'success', StatusMsgs.get(100),
            {'auth': user_auth, 'rtx_id': user_res.get('rtx_id')}
        ).json()

    def update_user_by_rtx(self, data: dict) -> dict:
        """
        update user info by rtx id
        data: user info data
        """
        if not data:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()
        rtx_id = data.get('rtx_id')
        if not rtx_id:
            return Status(
                212, 'failure', u'缺少rtx_id请求参数', {}
            ).json()
        new_data = dict()
        for k, v in data.items():
            if not v or k == 'rtx_id': continue
            if k not in self.update_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if k == 'name':
                new_data['fullname'] = v
            elif k == 'rtx_id':
                new_data[k] = str(v).strip()
            else:
                new_data[k] = v

        user_model = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        if not user_model:
            return Status(
                302, 'failure', u'用户不存在' or StatusMsgs.get(302), {}
            ).json()
        for _k, _v in new_data.items():
            if not _k: continue
            setattr(user_model, _k, _v)
        self.sysuser_bo.merge_model_no_trans(user_model)
        new_user_model = self._model_to_dict(user_model) or {}
        if new_user_model.get('password'):
            del new_user_model['password']
        return Status(
            100, 'success', StatusMsgs.get(100), new_user_model
        ).json()

    def update_password_by_rtx(self, data):
        """
        update user password by rtx id
        data: user password data
        """
        if not data:
            return Status(
                212, 'failure', StatusMsgs.get(212), {}
            ).json()
        rtx_id = data.get('rtx_id')
        if not rtx_id:
            return Status(
                212, 'failure', u'缺少rtx_id请求参数', {}
            ).json()
        new_data = dict()
        for k, v in data.items():
            if not v or k == 'rtx_id': continue
            if k not in self.password_attrs:
                return Status(
                    213, 'failure', u'请求参数%s不合法' % k, {}
                ).json()
            if not v:
                return Status(
                    214, 'failure', u'请求参数%s不允许为空' % k, {}
                ).json()
            new_data[k] = v

        user_model = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        if not user_model:
            return Status(
                302, 'failure', u'用户不存在' or StatusMsgs.get(302), {}
            ).json()
        old_password = new_data.get('old_password')
        new_password = new_data.get('new_password')
        con_password = new_data.get('con_password')
        if old_password != user_model.password:
            return Status(
                232, 'failure', u'输入的旧密码有误' or StatusMsgs.get(232), {}
            ).json()
        if new_password != con_password:
            return Status(
                233, 'failure', u'两次新密码不一致' or StatusMsgs.get(233), {}
            ).json()
        setattr(user_model, 'password', new_password)
        self.sysuser_bo.merge_model_no_trans(user_model)
        new_user_model = self._model_to_dict(user_model) or {}
        if new_user_model.get('password'):
            del new_user_model['password']
        return Status(
            100, 'success', StatusMsgs.get(100), new_user_model
        ).json()

    def update_avatar_by_rtx(self, rtx_id, image_file):
        """
        update user avatar by rtx id
        rtx_id: user rtx id
        avatar: user avatar
        """
        if not rtx_id:
            return Status(
                212, 'failure', u'缺少rtx_id请求参数', {}
            ).json()
        if not image_file:
            return Status(
                212, 'failure', u'缺少上传文件', {}
            ).json()

        try:
            image_name = image_file.filename
            if not self.image_lib.allow_format_img(image_name):
                return Status(
                    401, 'failure', u'图片格式不支持' or StatusMsgs.get(401), {}
                ).json()
            # 本地存储
            local_res = self.image_lib.store_local(image_file, compress=False)
            if local_res.get('status_id') != 100:
                return Status(local_res.get('status_id'),
                              'failure',
                              local_res.get('message') or StatusMsgs.get(local_res.get('status_id')),
                              {}).json()
            local_image_file = local_res.get('data').get('file')
            # TODO 判断图片大小限制
            # image_info = self.image_lib.scan(local_image_file)
            
            # 上传store
            store_image_name = '%s/%s' % (get_now(format="%Y%m%d"), local_res.get('data').get('name'))
            store_res = self.store_lib.upload(store_name=store_image_name, local_file=local_image_file)
            if store_res.get('status_id') != 100:
                return Status(store_res.get('status_id'),
                              'failure',
                              store_res.get('message') or StatusMsgs.get(store_res.get('status_id')),
                              {}).json()

            user_model = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
            avatar = store_res.get('data').get('url')
            setattr(user_model, 'avatar', avatar)
            self.sysuser_bo.merge_model_no_trans(user_model)
            return Status(
                100, 'success', StatusMsgs.get('100'), {'avatar': avatar}
            ).json()

        except Exception as e:
            LOG.error('upload image save failure: %s' % e)
            return Status(
                501, 'failure',
                StatusMsgs.get(501) or u'服务端API请求发生故障，请稍后尝试',
                {}
            ).json()



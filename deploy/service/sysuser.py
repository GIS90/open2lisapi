# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    sysuser service

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 4:15 下午"
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
from deploy.bo.sysuser import SysUserBo
from deploy.bo.menu import MenuBo
from deploy.bo.role import RoleBo
from deploy.service.menu import MenuService
from deploy.utils.utils import d2s, get_now, check_length
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs, StatusEnum
from deploy.utils.logger import logger as LOG
from deploy.config import ADMIN, O_NOBN, \
    STORE_SPACE_NAME, STORE_BASE_URL, \
    USER_DEFAULT_AVATAR
from deploy.delib.store_lib import StoreLib
from deploy.delib.image_lib import ImageLib
from deploy.utils.verify import decode_access_token_rtx


class SysUserService(object):
    """
    sysuser service
    """

    base_attrs = ['id', 'rtx_id', 'md5_id', 'fullname', 'password',
                  'email', 'phone', 'avatar', 'introduction',
                  'department', 'role', 'is_del']

    extend_attrs = ['create_time', 'create_rtx', 'delete_time', 'delete_rtx']

    update_attrs = ['name', 'email', 'phone', 'introduction']

    password_attrs = ['old_password', 'new_password', 'con_password']

    def __init__(self):
        """
        SysUserServices class initialize
        """
        super(SysUserService, self).__init__()
        # bo
        self.sysuser_bo = SysUserBo()
        self.menu_bo = MenuBo()
        self.role_bo = RoleBo()
        # service
        self.menu_service = MenuService()
        # lib
        self.store_lib = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)
        self.image_lib = ImageLib()

    def __str__(self):
        print("SysUserService class.")

    def __repr__(self):
        self.__str__()

    def _model_to_dict(self, model, _type: str = 'base') -> dict:
        """
        user model transfer to dict data
        model: user model

        format user object
        """
        if not model:
            return {}
        if _type == 'base':
            attrs = self.base_attrs
        elif _type == 'all':
            attrs = self.base_attrs + self.extend_attrs
        else:
            attrs = self.base_attrs
        _res = dict()
        for attr in attrs:
            if attr == 'id':
                _res[attr] = model.id
            elif attr == 'rtx_id':
                _res[attr] = model.rtx_id
            elif attr == 'md5_id':
                _res[attr] = model.md5_id
            elif attr == 'fullname':
                _res['name'] = model.fullname
            elif attr == 'password':
                _res[attr] = model.password
            elif attr == 'email':
                _res[attr] = model.email or ""
            elif attr == 'phone':
                _res[attr] = model.phone or ""
            elif attr == 'avatar':
                _res[attr] = model.avatar or USER_DEFAULT_AVATAR
            elif attr == 'introduction':
                _res[attr] = model.introduction or ""
            elif attr == 'department':
                _res[attr] = model.department or ""
            elif attr == 'role':    # 多角色，存储role的engname，也就是role的rtx_id
                _res[attr] = str(model.role).split(';') if model.role else []
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
        return dict object data
        """
        user_res = dict()
        if not rtx_id:
            return user_res

        user = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        return self._model_to_dict(user, _type='base') if user else user_res

    def get_login_by_rtx(self, rtx_id: str) -> dict:
        """
        get login user by rtx id
        return dict object data
        rtx_id参数为rtx_id、phone、email
        多信息登录
        """
        user_res = dict()
        if not rtx_id:
            return user_res

        user = self.sysuser_bo.get_user_by_params(rtx_id)   # 用户多参登录方法
        return self._model_to_dict(user, _type='base') if user else user_res

    def get_user_by_token(self, token: str, is_vue: bool = False) -> dict:
        """
        get user model by token
        return dict object data

        token is user md5-id
        """
        pass

    def get_login_by_token(self, token: str) -> dict:
        """
        get login user model by token
        token: user token
        """
        # no token, return
        if not token:
            return Status(
                400, StatusEnum.FAILURE.value, "用户Token参数不存在", {}).json()

        # -------------------- check data --------------------
        token = token.strip()   #去空格
        # 验证jwt token
        rtx_id = decode_access_token_rtx(token)
        if not rtx_id:
            return Status(
                200, StatusEnum.FAILURE.value, StatusMsgs.get(200), {}).json()

        user = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        # user model is not exist
        if not user:
            return Status(
                202, StatusEnum.FAILURE.value, '用户未注册', {}).json()
        user_model = self._model_to_dict(user, _type='base')
        # user model is deleted
        if user_model.get('is_del'):
            return Status(
                203, StatusEnum.FAILURE.value, '用户已注销', {}).json()

        LOG.info('current login user rtx_id >>>>>>>>>> %s' % user_model.get('rtx_id') or O_NOBN)
        # delete password information
        if user_model.get('password'):
            del user_model['password']

        return Status(
            100, StatusEnum.SUCCESS.value, StatusMsgs.get(100), {'user': user_model, 'token': token} or {}
        ).json()

    def get_login_auth_by_rtx(self, rtx_id: str) -> dict:
        """
        get login auth model by rtx
        rtx_id: user rtx id
        """
        # ==================== check parameters ====================
        # not rtx_id parameter, return
        if not rtx_id:
            return Status(
                4001, StatusEnum.FAILURE.value, '缺少RTX-ID请求参数', {}).json()
        # -------------------- check user data --------------------
        rtx_id = rtx_id.strip()  # 去空格
        # get user by rtx
        user = self.sysuser_bo.get_auth_by_rtx(rtx_id)
        # user model is not exist
        if not user:
            return Status(
                202, StatusEnum.FAILURE.value, '用户未注册', {}).json()
        # user model is deleted
        user_res = self._model_to_dict(user, _type='base')
        if user_res.get('is_del'):
            return Status(
                203, StatusEnum.FAILURE.value, '用户已注销', {}).json()

        # -------------------- user auth --------------------
        # 判断是否管理员，如果是管理员是全部菜单权限
        # 多角色，if包含管理员，直接是管理员权限
        is_admin = True if ADMIN in user_res.get('role')\
            else False
        auth_list = list()
        if not is_admin:
            # get authority by role list
            # user is admin, not get role, all authority menu
            role_models = self.role_bo.get_models_by_engnames(user_res.get('role'))
            for _r in role_models:
                if not _r or not _r.authority: continue
                auth_list.extend([int(x) for x in _r.authority.split(';') if x])
            auth_list = list(set(auth_list))    # 去重
        # get authority menu tree
        user_auth = self.menu_service.get_routes(auth_list, is_admin) or []
        LOG.info('current login auth rtx_id >>>>>>>>>> %s' % user_res.get('rtx_id') or O_NOBN)
        return Status(
            100, StatusEnum.SUCCESS.value, StatusMsgs.get(100),
            {'auth': user_auth, 'rtx_id': user_res.get('rtx_id')}
        ).json()

    def update_user_by_rtx(self, data: dict) -> dict:
        """
        update user info by rtx id
        data: user info data
        """
        # check parameters
        if not data:
            return Status(
                400, StatusEnum.FAILURE.value, StatusMsgs.get(400), {}).json()
        rtx_id = data.get('rtx_id')
        if not rtx_id:
            return Status(
                4001, StatusEnum.FAILURE.value, '缺少RTX-ID请求参数', {}).json()

        rtx_id = str(rtx_id).strip()    # 去空格
        new_data = dict()
        for k, v in data.items():
            if k == 'rtx_id': continue
            # illegal
            if k not in self.update_attrs:
                return Status(
                    401, StatusEnum.FAILURE.value, '请求参数%s不合法' % k, {}).json()
            # check: value is not null
            if not v and k not in ['email', 'introduction']:
                return Status(
                    403, StatusEnum.FAILURE.value, '请求参数%s不允许为空' % k, {}).json()
            # check: length
            if k == 'name' and not check_length(v, 30):
                return Status(
                    405, StatusEnum.FAILURE.value, '请求参数%s长度超出限制' % k, {}).json()
            elif k == 'phone' and len(v) != 11:
                return Status(
                    404, StatusEnum.FAILURE.value, '正确电话为11位', {}).json()
            elif k == 'email' and not check_length(v, 35):
                return Status(
                    405, StatusEnum.FAILURE.value, '请求参数%s长度超出限制' % k, {}).json()
            elif k == 'introduction' and not check_length(v, 255):
                return Status(
                    405, StatusEnum.FAILURE.value, '请求参数%s长度超出限制' % k, {}).json()
            if k == 'name':
                new_data['fullname'] = v
            elif k == 'rtx_id':
                new_data[k] = str(v).strip()    # rtx_id 去空格
            else:
                new_data[k] = v

        user_model = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        # user model is not exist
        if not user_model:
            return Status(
                501, StatusEnum.FAILURE.value, '数据不存在', {"rtx_id": rtx_id}).json()
        # TODO 添加注销用户判断
        for _k, _v in new_data.items():
            if not _k: continue
            setattr(user_model, _k, _v)
        self.sysuser_bo.merge_model_no_trans(user_model)
        # update user data return latest data information
        new_user_model = self._model_to_dict(user_model) or {}
        # delete password information
        if new_user_model.get('password'):
            del new_user_model['password']
        return Status(
            100, StatusEnum.SUCCESS.value, StatusMsgs.get(100), new_user_model).json()

    def update_password_by_rtx(self, data):
        """
        update user password by rtx id, password contain:
            - new password
            - confirm password
            - old password
        data: user password data
        """
        # check parameters
        if not data:
            return Status(
                400, StatusEnum.FAILURE.value, StatusMsgs.get(400), {}).json()
        rtx_id = data.get('rtx_id')
        if not rtx_id:
            return Status(
                4001, StatusEnum.FAILURE.value, '缺少RTX-ID请求参数', {}).json()
        # ---------------- parameters format ------------------
        rtx_id = str(rtx_id).strip()    # 去空格
        new_data = dict()
        for k, v in data.items():
            if k == 'rtx_id': continue
            if k not in self.password_attrs:
                return Status(
                    401, StatusEnum.FAILURE.value, '请求参数%s不合法' % k, {}).json()
            if not v:
                return Status(
                    403, StatusEnum.FAILURE.value, '请求参数%s不允许为空' % k, {}).json()
            new_data[k] = v

        # get user model
        user_model = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
        if not user_model:
            return Status(
                202, StatusEnum.FAILURE.value, '用户不存在', {}).json()

        # 老密码、新密码、确认密码进行验证
        old_password = new_data.get('old_password')
        new_password = new_data.get('new_password')
        con_password = new_data.get('con_password')
        # 老密码不同
        if old_password != user_model.password:
            return Status(
                206, StatusEnum.FAILURE.value, '用户输入的旧密码有误', {}).json()
        # 2次新密码不一致
        if new_password != con_password:
            return Status(
                207, StatusEnum.FAILURE.value, '输入的两次新密码不一致', {}).json()

        # update user password
        setattr(user_model, 'password', new_password)
        self.sysuser_bo.merge_model_no_trans(user_model)
        new_user_model = self._model_to_dict(user_model) or {}
        if new_user_model.get('password'):
            del new_user_model['password']
        return Status(
            100, StatusEnum.SUCCESS.value, StatusMsgs.get(100), new_user_model).json()

    def update_avatar_by_rtx(self, rtx_id, image_file):
        """
        update user avatar by rtx id
        rtx_id: user rtx id
        avatar: user avatar
        """
        # check parameters
        if not rtx_id:
            return Status(
                4001, StatusEnum.FAILURE.value, '缺少RTX-ID请求参数', {}).json()
        if not image_file:
            return Status(
                450, StatusEnum.FAILURE.value, '缺少上传文件', {}).json()

        try:
            image_name = image_file.filename
            # ============= image format check =============
            if not self.image_lib.allow_format_img(image_name):
                return Status(
                    454, StatusEnum.FAILURE.value, '图片格式不支持', {}).json()
            # ============= local store =============
            local_res = self.image_lib.store_local(image_file, compress=False)
            if local_res.get('status_id') != 100:
                return Status(local_res.get('status_id') or 456,
                              StatusEnum.FAILURE.value,
                              local_res.get('message') or "文件本地存储失败",
                              {}).json()
            local_image_file = local_res.get('data').get('file')
            # TODO 判断图片大小限制
            # image_info = self.image_lib.scan(local_image_file)
            
            # ============= upload store =============
            store_image_name = '%s/%s' % (get_now(format="%Y%m%d"), local_res.get('data').get('name'))
            store_res = self.store_lib.upload(store_name=store_image_name, local_file=local_image_file)
            if store_res.get('status_id') != 100:
                return Status(store_res.get('status_id') or 457,
                              StatusEnum.FAILURE.value,
                              store_res.get('message') or "文件云存储失败",
                              {}).json()
            # ---------------- update user model ----------------
            user_model = self.sysuser_bo.get_user_by_rtx_id(rtx_id)
            avatar = store_res.get('data').get('url')
            setattr(user_model, 'avatar', avatar)
            self.sysuser_bo.merge_model_no_trans(user_model)
            return Status(
                100, StatusEnum.SUCCESS.value, StatusMsgs.get('100'), {'avatar': avatar}).json()

        except Exception as error:
            LOG.error('User upload image save failure: %s' % error)
            return Status(
                900, StatusEnum.FAILURE.value, "用户上传头像发生异常，请稍后尝试", {}
            ).json()

    def random_avatar_list(self, params):
        """
        all avatar list
        :params: request params
        :return: json data
        """
        pass

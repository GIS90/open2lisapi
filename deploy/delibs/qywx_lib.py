# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    企业微信消息通知
    腾讯企业微信官网提供一整套WebHook API接口，内容相当丰富，可以实现内部、第三方等各种各样的功能
    详情参考reference urls

base_info:
    __author__ = "PyGo"
    __time__ = "2022/11/13 21：09"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __project__ = "quality-inspect"

usage:
    qywx_lib = QYWXLib(corp_id=企业号标识, secret=管理组凭证密钥, agent_id=机器人应用ID)
    qywx_lib.send_to_user_by_markdown(to_user, message)

    初始化必须的参数：
        - corp_id: 企业号标识
        - secret: 管理组凭证密钥
        - agent_id: 机器人应用ID

design:
    运用requests模拟API请求，这里主要实现了2大请求：
        - ACCESS TOKEN：认证token获取
        - SEND MESSAGE：发送消息

reference urls:
  - ACCESS TOKEN：https://developer.work.weixin.qq.com/document/path/91039
  - 发送应用消息：https://developer.work.weixin.qq.com/document/path/90236
  - 全局错误码：https://developer.work.weixin.qq.com/document/path/90313#10649
  - 上传临时素材：https://developer.work.weixin.qq.com/document/path/90253
  - 上传图片：https://developer.work.weixin.qq.com/document/path/90256
  --------------------------------------------------------------------------------------
    企业微信API response：
    {
      "errcode" : 0,
      "errmsg" : "ok",
      "invaliduser" : "userid1|userid2",
      "invalidparty" : "partyid1|partyid2",
      "invalidtag": "tagid1|tagid2",
      "unlicenseduser" : "userid3|userid4",
      "msgid": "xxxx",
      "response_code": "xyzxyz"
    }
  --------------------------------------------------------------------------------------

ACCESS_TOKEN请求方式：POST（HTTPS）
请求地址： https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN

返回示例：
    {
      "errcode" : 0,
      "errmsg" : "ok",
      "invaliduser" : "userid1|userid2",
      "invalidparty" : "partyid1|partyid2",
      "invalidtag": "tagid1|tagid2",
      "unlicenseduser" : "userid3|userid4",
      "msgid": "xxxx",
      "response_code": "xyzxyz"
    }
    - errcode：返回码
    - errmsg：对返回码的文本描述内容
    - invaliduser：不合法的userid，不区分大小写，统一转为小写
    - invalidparty：不合法的partyid
    - invalidtag：不合法的标签id
    - unlicenseduser：没有基础接口许可(包含已过期)的userid
    - msgid：消息id，用于撤回应用消息
    - response_code：仅消息类型为“按钮交互型”，“投票选择型”和“多项选择型”的模板卡片消息返回，应用可使用response_code调用更新模版卡片消息接口，24小时内有效，且只能使用一次


- 错误码查询工具：https://open.work.weixin.qq.com/devtool/query
- 发消息API参考：https://developer.work.weixin.qq.com/document/path/90236
- MARKDOWN语法：https://developer.work.weixin.qq.com/document/path/90236#%E6%94%AF%E6%8C%81%E7%9A%84markdown%E8%AF%AD%E6%B3%95


python version:
    python3


Enjoy the good time everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python qywx_lib.py
# ------------------------------------------------------------
import requests
import json
import os

from deploy.delibs.http_lib import HttpLibApi
from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs
from deploy.config import QYWX_BASE_URL, QYWX_SEND_MESSAGE, \
    QYWX_ACCESS_TOKEN, QYWX_SEND_BACK, QYWX_TEMP_UPLOAD, QYWX_TEMP_GET
from deploy.utils.utils import get_file_size


class QYWXLib(object):
    """
    QYWX class
    """

    types = [
        'text',         # 文本
        'image',        # 图片消息
        'voice',        # 语音消息
        'video',        # 视频消息
        'file',         # 文件消息
        'textcard',     # 文本卡片消息
        'news',         # 图文消息
        'mpnews',       # 多图文消息（mpnews类型的图文消息，跟普通的图文消息一致，唯一的差异是图文内容存储在企业微信。多次发送mpnews，会被认为是不同的图文，阅读、点赞的统计会被分开计算。）
        'markdown',     # markdown消息
        'miniprogram_notice',     # 小程序通知消息
        'template_card@text_notice',              # 模板卡片消息 > 文本通知型
        'template_card@news_notice',              # 模板卡片消息 > 图文展示型
        'template_card@button_interaction',       # 模板卡片消息 > 按钮交互型
        'template_card@vote_interaction',         # 模板卡片消息 > 投票选择型
        'template_card@multiple_interaction',     # 模板卡片消息 > 多项选择型
    ]

    safe_kwagrs_types = [
        'text',   # 文本
        'image',  # 图片消息
        'video',  # 视频消息
        'file',   # 文件消息
        'mpnews'  # 图文消息
    ]

    enable_id_trans_kwagrs_types = [
        'text',         # 文本
        'textcard',     # 文本卡片消息
        'news',         # 图文消息
        'mpnews',       # 多图文消息
        'miniprogram_notice',  # 小程序通知消息
        'template_card@text_notice',              # 模板卡片消息 > 文本通知型
        'template_card@news_notice',              # 模板卡片消息 > 图文展示型
        'template_card@button_interaction',       # 模板卡片消息 > 按钮交互型
        'template_card@vote_interaction',         # 模板卡片消息 > 投票选择型
        'template_card@multiple_interaction',     # 模板卡片消息 > 多项选择型
    ]

    content_types = [
        'text',  # 文本
        'markdown'  # markdown消息
    ]

    temp_upload_types = [
        'image',     # 图片
        'voice',     # 语音
        'video',     # 视频
        'file',      # 普通文件
    ]

    temp_upload_types_verify = {
        'image': {
            'suffix': ['.jpg', '.jpeg', '.png'],
            'size': 10 * 1024 * 1024
        },
        'voice': {
            'suffix': ['.amr'],
            'size': 2 * 1024 * 1024
        },
        'video': {
            'suffix': [
                '.wmv', '.asf', '.asx',    # 微软视频
                '.rm', '.rmvb',   # Real Player
                '.mp4',      # MPEG视频
                '.3gp',      # 手机视频
                '.m4v', '.mov',   # Apple视频
                '.mpg', '.mpeg', '.mpe',   # MPEG视频
                '.avi', '.dat', '.mkv', '.flv', '.vob'  # 其他常见视频
            ],
            'size': 10 * 1024 * 1024
        },
        'file': {
            'suffix': [],
            'size': 20 * 1024 * 1024
        }
    }

    def __init__(self, corp_id, secret, agent_id):
        """
        Initialize parameter
        :param corp_id: 企业号标识
        :param secret: 管理组凭证密钥
        :param agent_id: 机器人应用ID
        """
        self.CORP_ID = corp_id
        self.SECRET = secret
        self.AGENT_ID = agent_id
        self.http = HttpLibApi(QYWX_BASE_URL)
        self.token = self.__init_token()   # 每次实例化调用初始化access token

    def __init_token(self):
        """
        Initialize access token
        :return: string

        请求方式： GET（HTTPS）
        请求地址： https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRET
            - ID：企业号标识
            - SECRET：管理组凭证密钥
        返回示例：
            {
               "errcode": 0,
               "errmsg": "ok",
               "access_token": "accesstoken000001",
               "expires_in": 7200
            }
            - errcode：出错返回码，为0表示成功，非0表示调用失败
            - errmsg：返回码提示语
            - access_token：获取到的凭证，最长为512字节
            - expires_in：凭证的有效时间（秒）

        ACCESS TOKEN API参考：https://developer.work.weixin.qq.com/document/path/91039

        TODO
        7200秒（2小时）后续优化为缓存机制，避免在有效期内频繁调用
        """
        data = {
            "corpid": self.CORP_ID,
            "corpsecret": self.SECRET
        }
        status, response = self.http.get_json(url=QYWX_ACCESS_TOKEN, params=data)
        if not status:
            return None
        return response.get("access_token") \
            if response.get("errcode") == 0 and response.get("errmsg") == "ok" else None

    def check_token(self):
        """
        check access token is or not available
        :return: bool
        """
        return True if self.token else False

    def format_content(self, ftype: str = 'text', content: dict = {}) -> dict:
        """
        根据发送消息的类型格式化消息体内容
        :param ftype: 消息体类型
        :param content: 消息体内容

        :return: json
        """
        new_content = dict()
        if not content:
            return new_content
        if ftype not in self.types:
            return new_content
        # 依据消息类型格式化数据
        if ftype in self.content_types:
            new_content['content'] = content.get('data')
            return new_content
        else:
            return new_content

    def send(self, to_user=[], to_party=[], to_tag=[],
             content={}, stype: str = 'text', **kwargs) -> json:
        """
        send message to user or part or tag list by the content of data
        :param to_user: 指定接收消息的成员，成员ID列表，最多支持100个，指定为"@all"，则向该企业应用的全部成员发送
        :param to_party: 指定接收消息的部门，部门ID列表，最多支持100个，指定为"@all"，则向该企业应用的全部成员发送
        :param to_tag: 指定接收消息的标签，标签ID列表，最多支持100个，指定为"@all"，则向该企业应用的全部成员发送
        :param stype: 消息类型，默认text文本类型
        :param content: 消息体内容
        :param kwargs: 其他key-value参数
        :return: json

        请求数据：
            {
               "touser" : "UserID1|UserID2|UserID3",
               "toparty" : "PartyID1|PartyID2",
               "totag" : "TagID1 | TagID2",
               "agentid": 1,
               "msgtype": 消息体类型,
               消息体类型: {
                    消息体
               },
               safe: 0,
               enable_id_trans: 0,
               "enable_duplicate_check": 0,
               "duplicate_check_interval": 1800
            }
        参数说明：
            参数	         是否必须	            说明
            touser	        否	            成员ID列表（消息接收者，多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为@all，则向关注该企业应用的全部成员发送
            toparty	        否	            部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
            totag	        否	            标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
            agentid	        是	            企业应用的id，整型。企业内部开发，可在应用的设置页面查看；第三方服务商，可通过接口 获取企业授权信息 获取该参数值
            msgtype	        是	            消息类型
            content	        是	            消息体
            enable_id_trans	否	            表示是否开启id转译，0表示否，1表示是，默认0。仅第三方应用需要用到，企业自建应用可以忽略。
            enable_duplicate_check	否	    表示是否开启重复消息检查，0表示否，1表示是，默认0
            duplicate_check_
            interval	否	表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时

        备注：
            touser、toparty、totag不能同时为空
        """
        """ --------------------- parameters check --------------------- """
        if not self.token:
            return Status(
                212, 'failure', '请检查access token是否获取成功', {}).json()
        if not isinstance(to_user, list) \
                or not isinstance(to_party, list) \
                or not isinstance(to_tag, list):
            return Status(
                213, 'failure', '接收用户或者部门参数必须为List类型', {}).json()
        if not any([to_user, to_party, to_tag]):
            return Status(
                212, 'failure', '缺少接收用户或者部门列表', {}).json()
        if not content:
            return Status(
                212, 'failure', '缺少消息内容', {}).json()
        if not isinstance(content, dict):
            return Status(
                213, 'failure', '消息体参数必须为Dict类型', {}).json()
        if stype not in self.types:
            return Status(
                213, 'failure', '消息类型错误', {}).json()
        """ ================== 默认参数 ================== """
        # 表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，2表示仅限在企业内分享，默认为0；注意仅mpnews类型的消息支持safe值为2，其他消息类型不支持
        safe = 0         # 默认值
        if kwargs.get('safe'):
            safe = kwargs.get('safe')
            if safe not in (0, 1):
                return Status(
                    213, 'failure', 'safe参数值不合法，只允许0或者1', {}).json()
        # 表示是否开启id转译，0表示否，1表示是，默认0。仅第三方应用需要用到，企业自建应用可以忽略
        enable_id_trans = 0  # 默认值
        if kwargs.get('enable_id_trans'):
            enable_id_trans = kwargs.get('enable_id_trans')
            if enable_id_trans not in (0, 1):
                return Status(
                    213, 'failure', 'enable_id_trans参数值不合法，只允许0或者1', {}).json()
        # 表示是否开启重复消息检查，0表示否，1表示是，默认0
        enable_duplicate_check = 0  # 默认值
        if kwargs.get('enable_duplicate_check'):
            enable_duplicate_check = kwargs.get('enable_duplicate_check')
            if enable_duplicate_check not in (0, 1):
                return Status(
                    213, 'failure', 'enable_duplicate_check参数值不合法，只允许0或者1', {}).json()
        # 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        duplicate_check_interval = 1800  # 默认值
        if kwargs.get('duplicate_check_interval'):
            duplicate_check_interval = kwargs.get('duplicate_check_interval')
            if duplicate_check_interval < 1 or duplicate_check_interval > 4 * 60 * 60:
                return Status(
                    213, 'failure', 'duplicate_check_interval参数值不合法，只允许1秒或者4小时', {}).json()
        # 参数 >>>>> 基础data对象参数
        format_content = self.format_content(ftype=stype, content=content)
        if not format_content:
            return Status(
                213, 'failure', '格式化的消息体为空', {}).json()
        # 发送的数据
        data = {
            "agentid": self.AGENT_ID,
            "msgtype": stype,
            stype: format_content,
            "enable_duplicate_check": enable_duplicate_check,
            "duplicate_check_interval": duplicate_check_interval
        }
        # 参数 >>>>> 用户
        if to_user:
            data['touser'] = "|".join(to_user)
        if to_party:
            data['toparty'] = "|".join(to_party)
        if to_tag:
            data['totag'] = "|".join(to_tag)
        # 参数 >>>>> 额外data对象参数
        if stype in self.safe_kwagrs_types:
            data['safe'] = safe
        if stype in self.enable_id_trans_kwagrs_types:
            data['enable_id_trans'] = enable_id_trans

        """ 
        --------------------- request 企业微信 server --------------------- 
        send main 
        """
        try:
            url = "%s?access_token=%s" % (QYWX_SEND_MESSAGE, self.token)
            status, response = self.http.post_json(url=url, data=data)
            if not status:
                return Status(
                    501, 'failure', response.get('errmsg'), response).json()
            if response.get("errcode") == 0 and response.get("errmsg") == "ok":
                return Status(
                    100, 'success', '成功', response).json()
            else:
                return Status(
                    501, 'failure', response.get('errmsg'), response).json()
        except:
            return Status(501, 'failure', StatusMsgs.get(501), {}).json()

    def sendback(self, message_id: str) -> json:
        """
        撤回24小时内通过发送应用消息接口推送的消息，仅可撤回企业微信端的数据

        :param message_id: 消息ID
        :return: json

        参数说明：
            参数	        必须	        说明
            access_token	是	            access_token
            msgid	        是	            消息ID

        参考示例：https://developer.work.weixin.qq.com/document/path/94867
        """
        """ --------------------- parameters check --------------------- """
        if not self.token:
            return Status(
                212, 'failure', '请检查access token是否获取成功', {}).json()
        if not message_id:
            return Status(
                212, 'failure', '缺少message_id参数', {}).json()
        if not isinstance(message_id, str):
            return Status(
                213, 'failure', 'message_id参数支持str类型', {}).json()

        # 发送的数据
        data = {
            "msgid": message_id
        }

        try:
            url = "%s?access_token=%s" % (QYWX_SEND_BACK, self.token)
            status, response = self.http.post_json(url=url, data=data)
            if not status:
                return Status(
                    501, 'failure', response.get('errmsg'), response).json()
            if response.get("errcode") == 0 and response.get("errmsg") == "ok":
                return Status(
                    100, 'success', '成功', response).json()
            else:
                return Status(
                    501, 'failure', response.get('errmsg'), response).json()
        except:
            return Status(501, 'failure', StatusMsgs.get(501), {}).json()

    def _verify_temp_upload_file(self, upload_type: str, upload_name: str, upload_file: str) -> json:
        """
        :param upload_type: upload type, contain:
        :param upload_name: upload file name
        :param upload_file: local exist upload file path

        检查规则：
          - 图片（image）：10MB，支持JPG,PNG格式
          - 语音（voice） ：2MB，播放长度不超过60s，仅支持AMR格式
          - 视频（video） ：10MB，支持MP4格式
          - 普通文件（file）：20MB
        """
        rule = self.temp_upload_types_verify.get(upload_type)
        if not rule:
            return False, '无此类型文件校验'

        if not upload_name:
            upload_name = os.path.split(upload_file)[-1]
        upload_name_suffix = os.path.splitext(upload_name)[-1]

        if rule.get('suffix') and upload_name_suffix not in rule.get('suffix'):
            return False, '文件格式不支持'
        if get_file_size(path=upload_file, unit='B') > rule.get('size'):
            return False, '文件超出限制'
        return True, ''

    def temp_upload(self, upload_type: str, upload_name: str, upload_file: str) -> json:
        """
        :param upload_type: upload type, contain:
            > 图片（image）
            > 语音（voice）
            > 视频（video）
            > 普通文件（file）
        :param upload_name: upload file name
        :param upload_file: local exist upload file path

        企业微信上传临时素材
          > 素材上传得到media_id，该media_id仅三天内有效
          > media_id在同一企业内应用之间可以共享

        大小限制：
          > 图片（image）：10MB，支持JPG,PNG格式
          > 语音（voice） ：2MB，播放长度不超过60s，仅支持AMR格式
          > 视频（video） ：10MB，支持MP4格式
          > 普通文件（file）：20MB

        请求方式：POST（HTTPS）
        请求地址：https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=ACCESS_TOKEN&type=TYPE

        参数	        必须	    说明
        access_token	是	        调用接口凭证
        type	        是	        媒体文件类型，分别有图片（image）、语音（voice）、视频（video），普通文件（file）

        相关URL：
          > 上传临时素材：https://developer.work.weixin.qq.com/document/path/90253
          > 上传图片：https://developer.work.weixin.qq.com/document/path/90256

        :return: json data
        """
        """ --------------------- parameters check --------------------- """
        if not self.token:
            return Status(
                212, 'failure', '请检查access token是否获取成功', {}).json()
        if not upload_type:
            return Status(
                212, 'failure', '缺少upload_type参数', {}).json()
        if not isinstance(upload_type, str):
            return Status(
                213, 'failure', 'upload_type参数支持str类型', {}).json()
        if upload_type not in self.temp_upload_types:
            return Status(
                213, 'failure', 'upload_type参数不支持请求类型', {}).json()
        if not upload_file \
                or not os.path.exists(upload_file) \
                or not os.path.isfile(upload_file):
            return Status(
                216, 'failure', '缺少上传文件', {}).json()
        # 无传入文件名称，自动获取上传文件的文件名称
        if not upload_name:
            upload_name = os.path.split(upload_file)[-1]

        """ --------------------- upload file suffix check --------------------- """
        # 上传文件类型检查
        verify_status, verify_message = self._verify_temp_upload_file(upload_type, upload_name, upload_file)
        if not verify_status:
            return Status(
                217, 'failure', verify_message, {}).json()

        """ --------------------- request 企业微信 server --------------------- """
        try:
            # read file stream
            with open(upload_file, 'rb') as f:
                file_content = f.read()
            files_body = {'media': (upload_name, file_content, 'text/plain')}
            url = "{}?access_token={}&type={}".format(QYWX_TEMP_UPLOAD, self.token, upload_type)
            headers = {
                'filename': upload_name,
                'Content-type': 'multipart/form-data;'
            }
            status, response = self.http.post_form(url=url, headers=headers, files=files_body)
            if not status:
                return Status(
                    501, 'failure', response.get('errmsg'), response).json()
            if response.get("errcode") == 0 and response.get("errmsg") == "ok":
                # 附件get地址
                response['url'] = "{}{}?access_token={}&media_id={}".format(QYWX_BASE_URL, QYWX_TEMP_GET, self.token, response.get('media_id'))
                return Status(
                    100, 'success', '成功', response).json()
            else:
                return Status(
                    501, 'failure', response.get('errmsg'), response).json()
        except:
            return Status(501, 'failure', StatusMsgs.get(501), {}).json()
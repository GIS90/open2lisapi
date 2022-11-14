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
from deploy.delibs.http_lib import HttpLibApi
from deploy.utils.status import Status
from deploy.config import QYWX_BASE_URL, QYWX_SEND_MESSAGE, QYWX_ACCESS_TOKEN


class QYWXLib(object):
    """
    QYWX class
    """
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

    def send_to_user_by_markdown(self, to_user: list, content: str, **kwargs):
        """
        用户私发消息 >>> markdown语法消息体

        send message to user list by the content of markdown type data
        :param to_user: 企业微信用户ID列表，列表类型参数
        :param content: markdown消息体
        :param kwargs: 其他key-value参数
        :return: json


        请求方式：POST（HTTPS）
        请求地址： https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN
            - ACCESS_TOKEN：access token
        请求数据：
            {
               "touser" : "UserID1|UserID2|UserID3",
               "toparty" : "PartyID1|PartyID2",
               "totag" : "TagID1 | TagID2",
               "msgtype": "markdown",
               "agentid" : 1,
               "markdown": {
                    "content": ""
               },
               "enable_duplicate_check": 0,
               "duplicate_check_interval": 1800
            }
        参数说明：
            参数	         是否必须	            说明
            touser	        否	            成员ID列表（消息接收者，多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为@all，则向关注该企业应用的全部成员发送
            toparty	        否	            部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
            totag	        否	            标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
            msgtype	        是	            消息类型，此时固定为：markdown
            agentid	        是	            企业应用的id，整型。企业内部开发，可在应用的设置页面查看；第三方服务商，可通过接口 获取企业授权信息 获取该参数值
            content	        是	            markdown内容，最长不超过2048个字节，必须是utf8编码
            enable_duplicate_check	否	    表示是否开启重复消息检查，0表示否，1表示是，默认0
            duplicate_check_interval	否	表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
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

        发消息API参考：https://developer.work.weixin.qq.com/document/path/90236
        MARKDOWN语法：https://developer.work.weixin.qq.com/document/path/90236#%E6%94%AF%E6%8C%81%E7%9A%84markdown%E8%AF%AD%E6%B3%95
        """
        if not self.token:
            return Status(212, 'failure', '请检查access token是否获取成功', {}).json()
        if not to_user:
            return Status(212, 'failure', '缺少用户列表', {}).json()
        if not isinstance(to_user, list):
            return Status(213, 'failure', '用户列表必须为List类型', {}).json()
        if not content:
            return Status(212, 'failure', '缺少消息内容', {}).json()

        data = {
            "touser": "|".join(to_user),
            "msgtype": "markdown",
            "agentid": self.AGENT_ID,
            "markdown": {
                "content": content
            },
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        url = "%s?access_token=%s" % (QYWX_SEND_MESSAGE, self.token)
        status, response = self.http.post_json(url=url, data=data)
        if not status:
            return Status(501, 'failure', response.get('errmsg'), {}).json()
        if response.get("errcode") == 0 and response.get("errmsg") == "ok":
            return Status(100, 'success', '成功', {}).json()
        else:
            return Status(501, 'failure', response.get('errmsg'), {}).json()

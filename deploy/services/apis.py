# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2023/9/7 21:01"
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
# usage: /usr/bin/python apis.py
# ------------------------------------------------------------
import json
import requests
import datetime


from deploy.utils.status import Status
from deploy.utils.status_msg import StatusMsgs


class ApisService(object):
    """
    apis service
    """

    API_KEY = "R4uejriAnLKV8x1IghtNa7gQ"
    SECRET_KEY = "Dm0Y0SRwX4ccL7c9iNsYwwYmkCHXGFGH"

    AI_APIS = {
        'ERNIE-Bot': "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions",
        'ERNIE-Bot-turbo': "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant",
        'Embedding-V1': "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1",
        'BLOOMZ-7B': "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/bloomz_7b1",
        'Qianfan-Chinese-Llama-2-7B': "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/qianfan_chinese_llama_2_7b",
    }

    def __init__(self):
        """
        ApisService class initialize
        """
        super(ApisService, self).__init__()

    def __str__(self):
        print("ApisService class")

    def __repr__(self):
        self.__str__()

    def get_access_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            'grant_type': "client_credentials",
            'client_id': self.API_KEY,
            'client_secret': self.SECRET_KEY
        }
        payload = json.dumps("")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, params=params, data=payload)
        if response.status_code == 200:
            return response.json().get('access_token')

    def ai_chat(self, params: dict) -> dict:
        """
        api: ai chat
        :return: json data
        """
        url = "%s?access_token=%s" % (self.AI_APIS.get('ERNIE-Bot-turbo'), self.get_access_token())

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": params.get('content')
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        res = {}
        if response.status_code == 200:
            json_resp = response.json()
            text = json_resp.get('result')
            created = json_resp.get('created')
            # print('%s: %s' % (datetime.datetime.fromtimestamp(created), text))
            res = {
                'time': created,
                'text': text
            }
        return Status(
            100, 'success', StatusMsgs.get(100), res
        ).json()


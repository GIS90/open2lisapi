# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    jwt token verify

base_info:
    __author__ = "PyGo"
    __time__ = "2024/10/16 20:49"
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
# usage: /usr/bin/python verify.py
# ------------------------------------------------------------
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta

from deploy.config import JWT_TOKEN_ALGORITHM, JWT_TOKEN_SECRET_KEY, JWT_TOKEN_EXPIRE_MINUTES
from deploy.utils.exception import JwtCredentialsException
from deploy.utils.utils import d2s, ts2d, d2ts, get_now_time


"""
# jwt token
JWT_TOKEN_SECRET_KEY = "Enjoy the good life everyday！！!"  # 密钥
JWT_TOKEN_ALGORITHM = "HS256"  # 算法
JWT_TOKEN_EXPIRE_MINUTES = 60 * 4   # 访问令牌过期时间，单位：分
"""


# 访问令牌过期时间（单位：分）
TOKEN_DEFAULT_EXPIRE_MINUTES = 60 * 4


def encode_access_token(rtx_id: str) -> None:
    """
    生成JWT TOKEN
    :param rtx_id: rtx-id
    :return: jwt token
    """
    if not rtx_id:
        return None

    to_encode_data = {"rtx_id": rtx_id}
    # token申请时间
    token_apply_time = get_now_time()
    to_encode_data['apply_time'] = d2s(token_apply_time, fmt="%Y-%m-%d %H:%M:%S")
    # token过期日期
    expire = token_apply_time + timedelta(minutes=JWT_TOKEN_EXPIRE_MINUTES or TOKEN_DEFAULT_EXPIRE_MINUTES)  # 如果没有配置默认登录时长，默认4h
    # expire = token_apply_time + timedelta(seconds=6)  # 调试
    expire_ts = d2ts(expire)
    to_encode_data['expire_time'] = d2s(expire, fmt="%Y-%m-%d %H:%M:%S")
    to_encode_data['expire_time_ts'] = expire_ts
    to_encode_data.update({"exp": expire_ts})
    # encode
    HEADERS = {"alg": "HS256", "typ": "JWT"}
    try:
        encoded_jwt = jwt.encode(payload=to_encode_data, key=JWT_TOKEN_SECRET_KEY, algorithm=JWT_TOKEN_ALGORITHM, headers=HEADERS)
    except:
        raise JwtCredentialsException("The credentials token [encode] is failure.")
    """
    jwt.encode参数解析：
        payload: dict[str, Any],
        key: AllowedPrivateKeys | str | bytes,
        algorithm: str | None = "HS256",
        headers: dict[str, Any] | None = None,
        json_encoder: type[json.JSONEncoder] | None = None,
        sort_headers: bool = True,
    ----------------------------------------------------------------------
    返回值：
        str：加密形成的Token字符串
    """
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    解密JWT TOKEN
    :param token: token
    :return: jwt payload
    """
    res = dict()
    if not token:
        return res

    try:
        decode_jwt = jwt.decode(jwt=token, key=JWT_TOKEN_SECRET_KEY, algorithms=[JWT_TOKEN_ALGORITHM])
    except (ExpiredSignatureError, InvalidTokenError):
        return res
    except Exception:
        raise JwtCredentialsException("The credentials token [decode] is failure.")
    """
    jwt.decode参数解析：
        jwt (str): Token字符串
        key (str or dict): 定义Token时的密钥
        algorithms (str or list): 定义Token时的算法
    ----------------------------------------------------------------------
    返回值：
        str: 解码加密后Token的rtx_id
    """
    return decode_jwt


def decode_access_token_rtx(token: str) -> None:
    """
    解密JWT TOKEN的RTX-ID
    :param token: token
    :return: rtx-id
    """
    if not token: return None
    return decode_access_token(token).get('rtx_id')


def verify_access_token_expire(token: str) -> (bool, str):
    """
    验证JWT TOKEN是否过期
    :param token: token
    :return: bool
    """
    if not token:
        return True, None

    try:
        decode_jwt = jwt.decode(jwt=token, key=JWT_TOKEN_SECRET_KEY, algorithms=[JWT_TOKEN_ALGORITHM])
        rtx_id = decode_jwt.get("rtx_id")
        exp = decode_jwt.get("exp")
        exp_datetime = ts2d(st=exp)
        now_datetime = get_now_time()
        return False if now_datetime < exp_datetime else True, rtx_id
    except (ExpiredSignatureError, InvalidTokenError):
        return True, None
    except Exception:
        raise JwtCredentialsException("The credentials token [decode] is failure.")


def read_token_header(token: str) -> dict:
    """
    读取JWT TOKEN HEADER信息
    :param token: token
    :return: header dict
    """
    header = dict()
    if not token:
        return header

    try:
        header = jwt.get_unverified_header(token)
    except:
        pass
    return header


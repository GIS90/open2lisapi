# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    public utils method
    任何项目、模块均都可以调用，均属于通用方法
    持续累计更新......

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/1/16"
    __mail__ = "mingliang.gao@163.com"
    __project__ = "open2lisapi"

usage:
    from utils import xxxx
    xxxx(p1, p2, ...)

design:
    具体方法详情请参考注释

reference urls:

python version:
    python3


Enjoy the good time everyday！！!
Life is short, I use python.

------------------------------------------------
"""
import os
import sys
import inspect
import hashlib
import time
import subprocess
import platform
from datetime import datetime, timedelta
from pathlib import Path as pathlib_path, PurePath as pathlib_purepath
# from functools import wraps
from flask import session
from deploy.config import ADMIN, ADMIN_AUTH_LIST


def get_cur_folder():
    """
    get current folder, solve is or not frozen of the script

    :return: the file current folder
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(__file__))
    else:
        cur_folder = os.path.dirname(inspect.getfile(inspect.currentframe()))
        return os.path.abspath(cur_folder)


def md5(v):
    """
    字符串md5加密

    :param v: value
    :return: md5 value
    """
    if isinstance(v, str):
        v = v.encode('utf-8')
    return hashlib.md5(v).hexdigest()


def s2d(s, fmt="%Y-%m-%d %H:%M:%S"):
    """
    字符串转日期

    :param s: string type time
    :param fmt: transfer to formatter
    :return: datetime type time
    """
    return datetime.strptime(s, fmt)


def d2s(d, fmt="%Y-%m-%d %H:%M:%S"):
    """
    日期转字符串

    :param d: datetime type time
    :param fmt: transfer to formatter
    :return: string type time
    """
    return d.strftime(fmt)


def d2ts(d):
    """
    日期转ts

    :param d: datetime type parameter
    :return: time.time type
    """
    return time.mktime(d.timetuple())


def s2ts(s, format="%Y-%m-%d %H:%M:%S"):
    """
    字符串转ts

    :param s: sting type parameter
    :return: time.time type
    """
    d = s2d(s, format)
    return d2ts(d)


def dura_date(d1, d2, need_d=False):
    """
    get datetime1 and datetime2 difference

    :param d1: datetime parameter 1
    :param d2: datetime parameter 2
    :param need_d: is or not need hours, minutes, seconds
    :return: result 1: seconds
    result 2: hours, minutes, seconds
    """
    if type(d1) is str:
        d1 = s2d(d1)
    if type(d2) is str:
        d2 = s2d(d2)
    d = d2 - d1
    if need_d is False:
        seconds = d.seconds
        mins = seconds / 60.00
        hours = mins / 60.00
        return seconds, mins, hours
    return d


def get_now_time():
    """
    获取当前时间

    :return: to return the now of datetime type
    """
    return datetime.now()


def get_now_date():
    """
    获取当前日期

    :return: to return the now of date type
    """
    return datetime.now().date()


def get_now(format="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间，字符串类型

    :return: to return the now of string type
    """
    return d2s(datetime.now(), format)


def get_week_day(date):
    """
    today week

    :param date: date
    :return: week
    """
    weekdaylist = ('星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天')
    weekday = weekdaylist[date.weekday()]
    return weekday


def get_user_id():
    """
    get current request link user rtx id
    :return: rtx id or None
    """
    return session.get('rtx-id') or session.get('user_id')


def get_real_ip(request):
    """
    get request real ip

    :param request: flask api request object
    """
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]
    return ip


def get_rtx_id(request):
    """
    get request user rtx-id

    :param request: flask api request object
    """
    return request.headers.get("X-Rtx-Id") \
        if request.headers.get("X-Rtx-Id") else ''


def mk_dirs(path):
    """
    make folder（递归方式）

    :param path: to make folder path
    :return: path
    """
    os.makedirs(path)
    return path


def get_deploy_dir():
    """
    获取项目deploy目录

    :return: abs deploy path
    """
    return os.path.dirname(get_cur_folder())


def get_root_dir():
    """
    获取项目root目录

    :return: project root directory
    """
    root = pathlib_path(__file__).resolve().parent.parent.parent
    if root.is_absolute() and pathlib_path.exists(root):
        return root
    else:
        return pathlib_path.cwd().resolve().parent.parent


def v2decimal(x, y):
    """
    保留小数

    :param x: value
    :param y: point decimal
    :return:
    """
    if not x:
        return None
    if x.find('.') > 0:
        return round(x, y)
    return int(x)


def get_month_list():
    """
    获取月份list

    :return: list data
    """
    return [u'1月', u'2月', u'3月', u'4月', u'5月', u'6月',
            u'7月', u'8月', u'9月', u'10月', u'11月', u'12月']


def filename2md5(rtx_id: str = None, file_name: str = None, _type: str = 'file'):
    """
    get local store file name by md5 value

    :param rtx_id: rtx id
    :param file_name: file name
    :param _type: file type, is file,image, and so on.
    :return:
    result is tuple
    param1: md5 value no suffix
    param2: md5 value have suffix
    """
    file_names = os.path.splitext(file_name)
    suffix = (file_names[1]).lower() if len(file_names) > 1 else ''
    _v = file_name + get_now() + _type + rtx_id if rtx_id \
        else file_name + get_now() + _type
    md5_v = md5(_v)
    return md5_v, md5_v + suffix if suffix else md5_v


def check_length(data, limit=10):
    """
    check data length

    :param data: check data
    :param limit: length limit, default value is 10
    return True or False
    """
    if not data:
        return True
    return True if len(data) <= limit else False


def get_day_week_date(query_date):
    """
    get query day current week
    :param query_date: query day, is str

    return dict
    format:
        - start_time
        - end_time
        - [星期一date, 星期二date, 星期三date, 星期四date, 星期五date, 星期六date, 星期日date]
    """
    if not query_date:
        query_date = get_now_date()
    if isinstance(query_date, str):
        query_date = s2d(query_date, fmt="%Y-%m-%d")
    current_week = query_date.isoweekday()  # 当前时间所在本周第几天
    start_week_date = (query_date - timedelta(days=current_week - 1))
    end_week_date = (query_date + timedelta(days=7 - current_week))
    _week = list()
    for day_num in range(0, 7, 1):
        _week.append(d2s(start_week_date + timedelta(days=day_num), fmt="%Y-%m-%d"))
    _res = {
        "start_week_date": d2s(start_week_date, fmt="%Y-%m-%d"),  # 本周起始日期
        "end_week_date": d2s(end_week_date, fmt="%Y-%m-%d"),  # 本周结束日期
        "week_date": _week  # 本周日期列表

    }
    return _res


def ping(ip: str, **kwargs):
    """
    insect to ping the ip connection

    :param ip: the target ip or 域名
    :param kwargs: the ping other parameters
    :return: bool

    **kwargs:
        -a             将地址解析为主机名。
        -n count       要发送的回显请求数。
        -l size        发送缓冲区大小。
        -w timeout     等待每次回复的超时时间(毫秒)。

    usage:
        ping(ip='www.baidu.com', n=4, w=2000, l=32)
        or
        ping(ip='127.0.0.1', n=4, w=2000, l=32)

    param default value:
        - count: 4
        - size: 32
        - timeout: 2000
    """
    cmd = ['ping']
    # **kwargs > ping > a
    if kwargs.get('a'):
        cmd.append('-a')
    # **kwargs > ping > n
    if kwargs.get('n') or kwargs.get('count'):
        count = kwargs.get('n') or kwargs.get('count') or 4
        if not isinstance(count, int):
            count = 4
        if count > 0:
            cmd.append('-n %s' % count)
    # **kwargs > ping > l
    if kwargs.get('l') or kwargs.get('size'):
        size = kwargs.get('l') or kwargs.get('size') or 32
        if not isinstance(size, int):
            size = 0
        if size > 0:
            cmd.append('-l %s' % size)
    # **kwargs > ping > w
    if kwargs.get('w') or kwargs.get('timeout'):
        timeout = kwargs.get('w') or kwargs.get('timeout') or 2000
        if not isinstance(timeout, int):
            timeout = 0
        if timeout > 0:
            cmd.append('-w %s' % timeout)
    cmd.append(ip)
    cmd_str = ' '.join(cmd)
    ret_res = subprocess.call(cmd_str, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    return True if ret_res == 0 else False


def host_os():
    """
    current run pc or server information
    windows: 1
    Linux: 2
    MacOS: 3

    :return: int, detail information
    """
    _host_os = platform.system()
    _host_bit = platform.architecture()
    if _host_os == 'Windows':
        os_code = 1
    elif _host_os == 'Linux':
        os_code = 2
    elif _host_os == 'Darwin':
        os_code = 3
    else:
        os_code = 4

    _detail = {
        'os': _host_os,
        'os_code': os_code,
        'bit': _host_bit[0] if len(_host_bit) > 1 else _host_bit
    }
    return os_code, _detail


def auth_rtx_join(rtx_list=None) -> list:
    """
    管理员特殊数据权限
    > 与config中的ADMIN_AUTH_LIST关联
    > 追加ADMIN
    > 追加传入的特殊用户列表

    参数只允许是list或者str
    """
    if rtx_list is None:
        rtx_list = []
    if not isinstance(rtx_list, list) \
            and not isinstance(rtx_list, str):
        rtx_list = []

    _new_list = list()
    # 特殊权限
    _new_list = ADMIN_AUTH_LIST.copy()  # 多层在用copy.deepcopy
    # 管理员
    _new_list.append(ADMIN)
    # 传入的权限操作账户RTX列表
    if rtx_list and isinstance(rtx_list, list):
        _new_list.extend(rtx_list)
    if rtx_list and isinstance(rtx_list, str):
        _new_list.append(rtx_list)
    return _new_list


def api_inspect_rtx() -> dict:
    """
    检查请求的API是否包含RTX-ID参数，不包含则中止请求
    POST请求：
        get_json()
    GET请求：
        args
    其他：
        no check
    """
    pass


def get_file_size(path, unit: str = 'KB'):
    """
    获取传入的文件大小，以默认KB大小返回
    """
    # not found file
    if not path \
            or not os.path.isfile(path) \
            or not os.path.exists(path):
        return 0

    # get the real file size
    size = os.path.getsize(path)
    if size == 0:
        return 0

    # return file size, default is KB
    __unit = str(unit).upper() if unit else 'KB'
    b = 1024
    if __unit == 'B':
        return size
    elif __unit == 'KB':
        return size / b
    elif __unit == 'MB':
        return size / b**2
    elif __unit == 'GB':
        return size / b**3
    elif __unit == 'TB':
        return size / b**4
    else:
        return size

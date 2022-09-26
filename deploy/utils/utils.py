# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe:
    the all collection of daily tools and methods
    main:
        path
        make dir
        date && time
        ......

usage:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/1/16"
    __mail__ = "mingliang.gao@163.com"
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
from functools import wraps
from flask import session
from deploy.utils.logger import logger as LOG


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
    return session.get('user-id') or session.get('rtx-d')


# 计时装饰器
def timeer(fn):
    @wraps(fn)
    def _wrapper(*args, **kwargs):
        start = datetime.now()
        res = fn(*args, **kwargs)
        end = datetime.now()
        LOG.info('@timeer %s is run: %s' % (fn.__name__, (end - start).seconds))
        return res

    return _wrapper


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


def get_base_dir():
    """
    获取项目base目录（deploy）

    :return: deploy base path
    """
    return os.path.dirname(get_cur_folder())


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
    host_os = platform.system()
    host_bit = platform.architecture()
    if host_os == 'Windows':
        os_code = 1
    elif host_os == 'Linux':
        os_code = 2
    elif host_os == 'Darwin':
        os_code = 3
    else:
        os_code = 4

    _detail = {
        'os': host_os,
        'os_code': os_code,
        'bit': host_bit[0] if len(host_bit) > 1 else host_bit
    }
    return os_code, _detail

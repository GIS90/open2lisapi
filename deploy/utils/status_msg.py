# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = "PyGo"
    __time__ = "2022/2/19 10:58 下午"
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
Life is short I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python status_msg.py
# ------------------------------------------------------------


StatusMsgs = {
    100: "成功",
    101: "请求成功，查询数据为空",
    200: "用户未登录",
    201: "用户密码输入错误",
    202: "用户未注册",
    203: "用户已注销",
    211: "请求方法错误",
    212: "缺少请求参数",
    213: "请求参数不合法",
    214: "请求参数为必须信息",
    215: "缺少rtx_id信息",
    216: "缺少上传文件",
    217: "文件格式不支持",
    218: "文件内容不符合要求",
    219: "文件行内容有问题",
    220: "文件本地存储失败",
    221: "文件数据已存在",
    222: "文件导出数据为空",
    223: "文件全部上传失败",
    224: "文件部分上传失败",
    225: "文件存储数据库记录失败",
    226: "文件不存在",
    227: "文件不存在数据",
    228: "文件超过65535行不能进行拆分",
    229: "超出操作的sheet索引",
    230: "文件存储目录不存在",
    231: "参数特殊要求",
    232: "输入的旧密码有误",
    233: "两次新密码不一致",
    234: "文件压缩有误",
    301: "数据已存在，无需重新建立",
    302: "数据不存在",
    303: "部分数据处理成功",
    304: "数据已删除，无需处理",
    305: "数据已处理，无须二次处理",
    306: "数据已删除，无须二次删除",
    307: "数据处理失败",
    308: "数据不可用",
    3081: "数据（地址）不可用",
    3082: "数据（姓名）不可用",
    3083: "数据（重量）不可用",
    3084: "数据（电话）不可用",
    309: "数据创建用户与当前更改用户不一致",
    310: "非数据相关人员，无权限更新",
    311: "数据非当前用户拥有，无权限删除",
    312: "不支持.xls文件",
    401: "图片格式不支持",
    402: "图片存储失败",
    403: "文章创建者与提交者不符合",
    450: "数据存储失败",
    500: "服务端发生故障，请联系管理员：mingliang.gao",
    501: "服务端API请求发生故障，请稍后尝试",
    601: "HTTP请求接口失败",
    602: "HTTP请求数据为空",
    603: "HTTP请求数据不可用",
    998: "方法异常，请检查",
    999: "其他问题原因"
}
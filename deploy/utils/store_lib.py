# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    对象存储
    使用了七牛（qiniu.com）面对对象存储，注册免费使用10G空间
    后期业务量上来之后，在考虑继续扩展或者更换其他对象存储的问题

    七牛账户：13051355646
    官网Python SDK：https://developer.qiniu.com/kodo/1242/python#1

    存储对象类型说明：
    对比项        标准存储                      低频存储                      归档存储
    特性          高可靠、高可用和高性能的        高可靠、高性能、较低成本的      极低成本的高可靠归档数据
                 对象存储服务		           实时访问存储服务              存储服务
    数据访问      实时访问ms级延迟               实时访问ms级延迟               数据需先解冻才能访问，解冻过程1～5分钟
    最短存储时间   无要求                        30天                         60天
    最小计量空间   无要求                        64KB                         64KB
    数据取回      免费                          按实际读取的数据量收费          按实际读取的数据量收费
                                               单位 GB	                    单位 GB

base_info:
    __author__ = "PyGo"
    __time__ = "2022/3/6 8:54 上午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "twtoolbox_isapi"

usage:
    if __name__ == '__main__':
        image_store = StoreLib(space_url=STORE_BASE_URL, space_name=STORE_SPACE_NAME)
        # 上传本地文件/图片
        result = image_store.upload(store_name='pygp2域名.jpg', local_file='/Users/gaomingliang/Pictures/_pygo2.top.certificate.jpg')
        print(result)
        # 上传本地文件/图片（带存储目录）
        result = image_store.upload(store_name='2022/pygp2域名.jpg', local_file='/Users/gaomingliang/Pictures/_pygo2.top.certificate.jpg')
        print(result)
        # 上传远程文件/图片
        result = image_store.scrapy(store_name='w.jpg', remote_url='http://pygo2.top/images/article_w.jpg')
        print(result)
        # 公开空间下载文件/图片
        result = image_store.open_download(store_name='pygp2域名.jpg')
        print(result)
        # 私有空间下载文件/图片
        result = image_store.private_download(store_name='pygp2域名.jpg')
        print(result)
        # 删除文件/图片
        result = image_store.delete(store_name='top.jpg')
        print(result)
        # 获取文件/图片信息
        result = image_store.get_file_info(store_name='isapi.png')
        print(result)
        # 存储对象的移动
        result = image_store.move(src_space_name='twtoolbox', src_store_name='isapi-move-1.png',
                                  tar_space_name='twtoolbox', tar_store_name='isapi-move-2.png', overwrite=False)
        print(result)
        # 存储对象的复制
        result = image_store.copy(src_space_name='twtoolbox', src_store_name='isapi-move-2.png',
                                  tar_space_name='pygo-test-1', tar_store_name='isapi-move-space.png')
        print(result)

design:

reference urls:
    官网：https://developer.qiniu.com/kodo/1242/python
python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python store.py
# ------------------------------------------------------------
import os
import hashlib
import requests
from qiniu import Auth, put_file, BucketManager
from deploy.config import STORE_BASE_URL, STORE_ACCESS, \
    STORE_SECRET, STORE_SPACE_NAME
from datetime import datetime
from deploy.utils.status_msg import StatusMsgs


class StoreLib(object):
    """
    store lib in utils
    """
    def __init__(self, space_url, space_name):
        self.access_key = STORE_ACCESS
        self.secret_key = STORE_SECRET
        self.space_url = space_url or STORE_BASE_URL
        self.space_name = space_name or STORE_SPACE_NAME
        self.conn = self.__init_auth() or False
        self.manager = self.__init_bucket_manager() or False

    @staticmethod
    def format_res(status_id: int, message: str, data: dict) -> dict:
        """
        方法请求结果格式化
        """
        return {
            'status_id': status_id,
            'message': message if message else StatusMsgs.get(status_id),
            'data': data
        }

    def check(self) -> bool:
        """
        检查获取权限是否成功
        """
        return True if self.conn else False

    def __init_auth(self):
        """
        初始化Auth权限
        加入异常，以防止请求失败导致异常
        如果请求发生异常认定为初始化权限失败
        """
        try:
            return Auth(self.access_key, self.secret_key)
        except:
            return None

    def __new_token(self, space_name: str, store_name: str, timeout=120):
        """
        初始化上传文件的token
        """
        if not self.check():
            return None
        if not space_name or not store_name:
            return None
        try:
            return self.conn.upload_token(space_name, store_name, timeout)
        except:
            return None

    def __init_bucket_manager(self):
        """
        初始化一个bucket manager
        """
        return BucketManager(self.conn) if self.conn else None

    @staticmethod
    def get_now(fmt="%Y-%m-%d %H:%M:%S"):
        """
        字符串类型的当前时间
        """
        return datetime.now().strftime(fmt)

    @classmethod
    def new_now_store_name(cls, v) -> str:
        """
        用当前时间生成一个md5存储名称
        """
        if isinstance(v, str):
            v = v.encode('utf-8')
        return hashlib.md5(v).hexdigest()

    def upload(self, space_name: str = None, store_name: str = None, local_file: str = None,
               version: str = 'v2', timeout: int = 120) -> dict:
        """
        上传本地文件/图片的方法
        space_name：存储对象的空间名称
        store_name：存储对象的文件名称
        local_file：需要上传的本地文件
        version：断点续传的默认方法，默认为v2版本
        timeout：token存在时间，以秒为单位

        存储对象名称上带上目录/，存储的对象会自动创建对应目录
        """
        if not store_name:
            store_name = self.new_now_store_name(v=self.get_now())
        if not local_file:
            return self.format_res(
                212, '缺少上传文件参数', {}
            )

        if not os.path.exists(local_file) or \
                not os.path.isfile(local_file):
            return self.format_res(
                216, '上传文件不存在', {}
            )

        try:
            bucket_name = space_name if space_name \
                else self.space_name
            token = self.__new_token(bucket_name, store_name, timeout)
            if not token:
                return self.format_res(
                    601, 'Token创建失败，请检查网络或者对象存储配置', {}
                )

            ret, response = put_file(up_token=token, key=store_name, file_path=local_file, version=version)
            if response and response.status_code == 200:
                ret['url'] = '%s/%s' % (self.space_url, store_name)
                return self.format_res(
                    100, 'success', ret
                )
            else:
                return self.format_res(
                    999, 'Qiniu上传本地文件失败，请重新尝试', {}
                )
        except:
            return self.format_res(998, '方法异常，请检查', {})

    def scrapy(self, space_name: str = None, store_name: str = None, remote_url: str = None) -> dict:
        """
        上传远程或者网络上的文件/图片方法
        space_name：存储对象的空间名称
        store_name：存储对象的文件名称
        remote_url：需要上传的远程文件URL地址

        存储对象名称上带上目录/，存储的对象会自动创建对应目录
        """
        if not store_name:
            store_name = self.new_now_store_name(v=self.get_now())
        if not remote_url:
            return self.format_res(
                212, '缺少远程上传文件参数', {}
            )

        try:
            remote_response = requests.get(url=remote_url)
            if remote_response.status_code != 200:
                return self.format_res(
                    216, '上传文件不存在', {}
                )

            bucket_name = space_name if space_name \
                else self.space_name
            ret, response = self.manager.fetch(remote_url, bucket_name, store_name)
            if response and response.status_code == 200:
                ret['url'] = '%s/%s' % (self.space_url, store_name)
                return self.format_res(
                    100, 'success', {'key': store_name}
                )
            else:
                return self.format_res(
                    999, 'Qiniu上传远程文件失败，请重新尝试', {}
                )
        except:
            return self.format_res(998, '方法异常，请检查', {})

    def open_download(self, space_url: str = None, store_name: str = None) -> dict:
        """
        公开空间下载文件/图片的方法
        space_url：存储对象空间的域名
        store_name：存储对象的文件名称（包含目录）
        """
        if not store_name:
            return self.format_res(
                212, '缺少删除文件参数', {}
            )

        try:
            bucket_url = space_url if space_url \
                else self.space_url
            dl_url = '%s/%s' % (bucket_url, store_name)
            response = requests.get(dl_url)
            if response and response.status_code == 200:
                return self.format_res(
                    100, 'success', {'key': store_name, 'url': dl_url}
                )
            if response and response.status_code == 404:
                return self.format_res(
                    100, '对象不存在', {}
                )
            else:
                return self.format_res(
                    999, 'Qiniu下载失败，请重新尝试', {}
                )
        except:
            return self.format_res(998, '方法异常，请检查', {})

    def private_download(self, space_url: str = None, store_name: str = None, timeout: int = 120) -> dict:
        """
        私有空间下载文件/图片的方法
        space_url：存储对象空间的域名
        store_name：存储对象的文件名称（包含目录）
        timeout：超时时间，以秒为单位
        """
        if not self.check():
            return self.format_res(601, 'Auth鉴权失败，请检查网络或者对象存储配置', {})
        if not store_name:
            return self.format_res(212, '缺少删除文件参数', {})

        try:
            bucket_url = space_url if space_url \
                else self.space_url
            dl_url = '%s/%s' % (bucket_url, store_name)
            private_url = self.conn.private_download_url(dl_url, expires=timeout)
            response = requests.get(private_url)
            if response and response.status_code == 200:
                return self.format_res(100, 'success', {'key': store_name, 'url': private_url})
            if response and response.status_code == 404:
                return self.format_res(100, '对象不存在', {})
            else:
                return self.format_res(999, 'Qiniu下载失败，请重新尝试', {})
        except:
            return self.format_res(998, '方法异常，请检查', {})

    def delete(self, space_name: str = None, store_name: str = None) -> dict:
        """
        删除文件/图片的方法
        space_name：存储对象的空间名称
        store_name：存储对象的文件名称（包含目录）

        如果目录无存储对象文件，目录会自动删除
        """
        if not self.manager:
            return self.format_res(999, 'BucketManager初始化失败', {})
        if not store_name:
            return self.format_res(212, '缺少删除文件参数', {})
        bucket_name = space_name if space_name \
            else self.space_name
        try:
            ret, response = self.manager.delete(bucket_name, store_name)
            if response and response.status_code == 200:
                return self.format_res(100, 'success', {'key': store_name})
            else:
                return self.format_res(999, 'Qiniu删除失败，请重新尝试', {})
        except:
            return self.format_res(998, '方法异常，请检查', {})

    def get_file_info(self, space_name: str = None, store_name: str = None) -> dict:
        """
        获取文件/图片的基本信息
        space_name：存储对象的空间名称
        store_name：存储对象的文件名称（包含目录）
        """
        if not self.manager:
            return self.format_res(
                999, 'BucketManager初始化失败', {}
            )
        if not store_name:
            return self.format_res(
                212, '缺少删除文件参数', {}
            )

        try:
            bucket_name = space_name if space_name \
                else self.space_name
            ret, response = self.manager.stat(bucket_name, store_name)
            if response and response.status_code == 200:
                return self.format_res(
                    100, 'success', ret
                )
            else:
                return self.format_res(
                    999, 'Qiniu删除失败，请重新尝试', {}
                )
        except:
            return self.format_res(998, '方法异常，请检查', {})

    def move(self, src_space_name: str = None, src_store_name: str = None,
             tar_space_name: str = None, tar_store_name: str = None,
             overwrite: bool = True) -> dict:
        """
        存储对象的移动，可以跨存储空间
        src_space_name: 原存储对象的空间名称
        src_store_name: 原存储对象的名称（包含目录）
        tar_space_name: 目标存储对象的空间名称
        tar_store_name: 目标存储对象的名称（包含目录）
        overwrite: 是否进行一个目标存储对象的同名文件覆盖，默认为True可以覆盖，
        如果为False，目标存储对象文件存在的话不覆盖，移动失败
        """
        if not self.manager:
            return self.format_res(999, 'BucketManager初始化失败', {})
        if not src_space_name:
            return self.format_res(212, '缺少原存储对象空间名称参数', {})
        if not src_store_name:
            return self.format_res(212, '缺少原存储对象名称参数', {})
        if not tar_space_name:
            return self.format_res(212, '缺少目标存储对象空间名称参数', {})
        if not tar_store_name:
            return self.format_res(212, '缺少目标存储对象名称参数', {})

        try:
            # TODO 源文件、目标文件的存在验证
            ret, response = self.manager.move(src_space_name,
                                              src_store_name,
                                              tar_space_name,
                                              tar_store_name)
            if response and response.status_code == 200:
                return self.format_res(
                    100, 'success', {'tarkey': tar_store_name, 'srckey': src_store_name}
                )
            else:
                return self.format_res(
                    999, 'Qiniu移动对象失败，请重新尝试', {}
                )
        except:
            return self.format_res(998, '方法异常，请检查', {})

    def copy(self, src_space_name: str = None, src_store_name: str = None,
             tar_space_name: str = None, tar_store_name: str = None) -> dict:
        """
        存储对象的移动，可以跨存储空间
        src_space_name: 原存储对象的空间名称
        src_store_name: 原存储对象的名称（包含目录）
        tar_space_name: 目标存储对象的空间名称
        tar_store_name: 目标存储对象的名称（包含目录）
        overwrite: 是否进行一个目标存储对象的同名文件覆盖，默认为True可以覆盖，
        如果为False，目标存储对象文件存在的话不覆盖，移动失败
        """
        if not self.manager:
            return self.format_res(999, 'BucketManager初始化失败', {})
        if not src_space_name:
            return self.format_res(212, '缺少原存储对象空间名称参数', {})
        if not src_store_name:
            return self.format_res(212, '缺少原存储对象名称参数', {})
        if not tar_space_name:
            return self.format_res(212, '缺少目标存储对象空间名称参数', {})
        if not tar_store_name:
            return self.format_res(212, '缺少目标存储对象名称参数', {})

        try:
            # TODO 源文件、目标文件的存在验证
            ret, response = self.manager.copy(src_space_name,
                                              src_store_name,
                                              tar_space_name,
                                              tar_store_name)
            if response and response.status_code == 200:
                return self.format_res(
                    100, 'success', {'tarkey': tar_store_name, 'srckey': src_store_name}
                )
            else:
                return self.format_res(
                    999, 'Qiniu复制对象失败，请重新尝试', {}
                )
        except:
            return self.format_res(998, '方法异常，请检查', {})

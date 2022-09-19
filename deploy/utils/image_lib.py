# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    image lib
    图片处理

base_info:
    __author__ = "PyGo"
    __time__ = "2022/3/8 7:49 下午"
    __version__ = "v.1.0.0"
    __mail__ = "gaoming971366@163.com"
    __blog__ = "www.pygo2.top"
    __project__ = "twtoolbox_isapi"

usage:
    image_lib = ImageLib()
    local_res = image_lib.store_local(image_file, compress=False)

design:

reference urls:

python version:
    python3


Enjoy the good life everyday！！!
Life is short, I use python.

------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python image_lib.py
# ------------------------------------------------------------
import os
from PIL import Image

from deploy.utils.utils import filename2md5, \
    get_now, mk_dirs
from deploy.config import STORE_CACHE, IMAGE_QUALITY, IMAGE_WIDTH
from deploy.utils.status_msg import StatusMsgs


class ImageLib(object):
    """
    image lib
    """
    ALLOWED_EXTENSIONS = [
            '.png',
            '.jpg',
            '.bmp',
            '.jpeg',
            '.gif',
            '.tif',
            '.psd'
        ]

    def __init__(self):
        """
        初始化参数
        暂无实例化参数，都从配置文件中进行获取
        """
        self.cache = STORE_CACHE
        self.quality = IMAGE_QUALITY
        self.width = IMAGE_WIDTH

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

    def allow_format_img(self, name):
        """
        image格式判断
        :param name: image name
        """
        names = os.path.splitext(name)
        if len(names) < 2:
            return True
        return True if (names[1]).lower() in self.ALLOWED_EXTENSIONS \
            else False

    @staticmethod
    def scan(image_file):
        """
        查看图片的基础信息
        image_file: image file
        """
        if not image_file or not os.path.exists(image_file):
            return {}

        img = Image.open(image_file)
        res = {
            'size': img.size,  # 大小
            'width': img.width,  # 图片的宽
            'height': img.height,  # 图片的高
            'format': img.format  # 图像格式
        }
        return res

    def store_local(self, image_file, compress=False):
        """
        图片本地化存储
        :param image_file: image file stream
        :param compress: image 是否进行压缩
        """
        if not image_file:
            return self.format_res(
                216, '文件不存在', {}
            )

        try:
            # ================= 文件存储初始化 =================
            now_date = get_now(format="%Y%m%d")
            real_store_dir = os.path.join(STORE_CACHE, now_date)
            if not os.path.exists(real_store_dir):
                mk_dirs(real_store_dir)
            # <<<<<<<<<<<<<<<<<< save image >>>>>>>>>>>>>>>>>>
            image_name = image_file.filename
            _, store_name_md5 = filename2md5(file_name=image_name, _type='image')
            image_real_file = os.path.join(real_store_dir, store_name_md5)
            image_file.save(image_real_file)
            # 是否进行图片压缩
            if compress:
                small_img = Image.open(image_real_file)
                w_percent = IMAGE_WIDTH / float(small_img.size[0])
                h_size = int(float(small_img.size[1]) * float(w_percent))
                small_img = small_img.resize((IMAGE_WIDTH, h_size), Image.ANTIALIAS)
                small_img.save(image_real_file, quality=IMAGE_QUALITY)
            return self.format_res(100, 'success',
                                   {'name': store_name_md5,
                                    'file': os.path.join(real_store_dir, store_name_md5)})
        except:
            return self.format_res(998, '图片存储失败', {})

    def update_size(self, image_file, length=280, width=280):
        """
        update image size: length with
        """
        if not image_file or \
                not os.path.exists(image_file):
            return self.format_res(
                216, '文件不存在', {})

        try:
            image_dir, image_name = os.path.split(image_file)
            out_file_md5, out_file_name = \
                filename2md5(file_name=image_name, _type='image')
            im = Image.open(image_file)
            out_image_file = os.path.join(image_dir, out_file_name)
            upsize_image = im.resize((length, width), Image.ANTIALIAS)
            upsize_image.save(out_image_file)
            return self.format_res(
                100, 'success', {'md5': out_file_md5, 'name': out_file_name})
        except:
            return self.format_res(
                998, '图片更新大小失败', {})


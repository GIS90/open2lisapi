# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    the file dealing lib

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/10/1 9:31 AM"
    __mail__ = "gaoming971366@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python file_lib.py
# ------------------------------------------------------------
import os
from multiprocessing import cpu_count
from pdf2docx import Converter

from deploy.utils.utils import get_storefilename_by_md5, \
    get_base_dir, get_now, mk_dirs
from deploy.config import TRANSFER_BASE_DIR


class FileLib(object):
    ALLOWED_EXTENSIONS = [
        '.doc',
        '.docx',
        '.xls',
        '.xlsx',
        '.ppt',
        '.pptx',
        '.pdf',
        '.txt',
    ]

    def __init__(self):
        """
        initialize parameters
        """
        self.cpu_count = cpu_count()

    def allow_format_fmt(self, fname):
        """
        build in function to check is or not file formatter
        :param fname:
        :return:
        """
        return True if (os.path.splitext(fname)[1]).lower() in self.ALLOWED_EXTENSIONS else False

    def store_file(self, file, compress=False, is_md5_store_name=True):
        """
        class main function
        to store file at server
        :param file: file object
        :param compress: file is or not to use compress
        :param is_md5_store_name: store name
        :return: False or True, json object
        result is tuple
        use False or True to judge request api is or not success
        if False, to print messgae
        """
        if not file:
            return False, {'message': '没有发现文件'}
        try:
            # 文件存储初始化
            now_date = get_now(format="%Y-%m-%d")
            real_store_dir = get_base_dir() + TRANSFER_BASE_DIR + now_date
            store_dir = os.path.join(TRANSFER_BASE_DIR + now_date)
            if not os.path.exists(real_store_dir):
                mk_dirs(real_store_dir)

            file_name = file.filename
            md5_v, _ = get_storefilename_by_md5(file_name, ftype='file')
            _real_file = os.path.join(real_store_dir, file_name)
            if os.path.exists(_real_file):
                file_name = '%s-%s%s' % (os.path.splitext(file_name)[0],
                                        get_now(format="%Y-%m-%d-%H-%M-%S"),
                                        os.path.splitext(file_name)[-1])
                _real_file = os.path.join(real_store_dir, file_name)
            file.save(_real_file)
            return True, {'name': file_name,
                          'store_name': file_name,
                          'md5': md5_v,
                          'path': os.path.join(store_dir, file_name),
                          'message': 'success'}
        except:
            return False, {'message': '文件存储发生错误'}

    def pdf_2_word(self, file_pdf: str, docx_name: str = None,
                   start: int = 0, end: int = None, pages: list = None,
                   is_multi_processing: bool = False, cpu_count: int = 1):
        """
        the pdf file to transfer to word format
        :param file_pdf: the pdf file object
        :param docx_name: transfer to store word file name
        :param start: transfer start page, default is 0
        :param end: transfer end page, default is max page
        :param pages: transfer page list, such as: [1, 2, 5]
        :param is_multi_processing: is or not start work many process
        :param cpu_count: cpu count, default is pc/server cpu + 1
        :return: json
        use pdf file to transfer to word file
        some parameter is not must, use default
        """
        if not file_pdf:
            return False, {'message': 'Pdf file is null', 'tar_file': ''}
        src_file = get_base_dir() + file_pdf
        if not os.path.exists(src_file):
            return False, {'message': 'Pdf file is not exist', 'tar_file': ''}
        if not os.path.isfile(src_file):
            return False, {'message': 'Pdf file is not file', 'tar_file': ''}
        if docx_name:
            docx_names = os.path.splitext(docx_name)
            if len(docx_names) < 2:
                return False, {'message': 'Pdf file name not have suffix', 'tar_file': ''}
        src_path, src_name = os.path.split(src_file)
        transfer_name_pdf = docx_name if docx_name else src_name
        transfer_name_word = os.path.splitext(transfer_name_pdf)[0] + '.docx'
        docx_file = os.path.join(src_path, transfer_name_word)
        rel_path = os.path.split(file_pdf)[0]
        tar_file = os.path.join(rel_path, transfer_name_word)
        # convert pdf to docx
        cv = Converter(src_file)
        # all pages by default
        if is_multi_processing and cpu_count >= self.cpu_count:
            cpu_count = self.cpu_count
        cv.convert(docx_file, multi_processing=True, cpu_count=cpu_count) \
            if is_multi_processing else cv.convert(docx_file)
        cv.close()
        return True, {'message': 'success', 'tar_file': tar_file}



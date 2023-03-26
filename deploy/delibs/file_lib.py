# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    文件处理包(the file dealing lib)
    静态工具包，适用于任何项目以及脚本
    开发于2020年，迭代更新


base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/10/1 9:31 AM"
    __mail__ = "gaoming971366@163.com"


Enjoy the good life everyday！！!
Life is short, I use python.


pdf2docx：https://dothinking.github.io/pdf2docx/quickstart.convert.html
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python file_lib.py
# ------------------------------------------------------------
import os
import json
import multiprocessing
from multiprocessing import cpu_count
from pdf2docx import Converter

from deploy.utils.utils import filename2md5, \
    get_now, mk_dirs, md5
from deploy.config import STORE_CACHE
from deploy.utils.status_msg import StatusMsgs


class FileLib(object):
    """
    file lib class
    """

    # file extension format
    # currently, only to support windows system file
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

    DOC_EXTENSIONS = [
        '.doc',
        '.docx'
    ]

    DPF_EXTENSIONS = [
        '.pdf'
    ]

    @staticmethod
    def _get_cpu_count():
        return cpu_count() - 1 or 1

    def __init__(self):
        """
        initialize parameters
        """
        self.default_doc_prefix = '.docx'
        self.cpu_count = self._get_cpu_count()

    @staticmethod
    def format_res(status_id: int, message: str, data: json) -> dict:
        """
        方法请求结果格式化
        """
        return {
            'status_id': status_id,
            'message': message if message else StatusMsgs.get(status_id),
            'data': data
        }

    def allow_format_fmt(self, filename):
        """
        build in function to check is or not file formatter
        :param filename: check file name
        :return: bool, True or False
        """
        return True if (os.path.splitext(filename)[1]).lower() in self.ALLOWED_EXTENSIONS else False

    def store_file(self, file, compress: bool = False, is_md5_store_name: bool = False):
        """
        file lib class main function, to store file at local

        :param file: file object
        :param compress: file is or not to use compress mode
        :param is_md5_store_name: store name is or not by md5 encryption
        :return: False or True, json object

        result is tuple
        use False or True to judge request api is or not success
        if False, to print message
        data structure:
            {
                name: file name,
                md5: file md5,
                store_name: store name, format is '%s/%s' % (now_date, file_name),
                path: path + store name
                message: result message
            }
        """
        if not file:
            return False, {'message': 'Not found file'}

        # 文件存储初始化
        now_date = get_now(format="%Y%m%d")
        real_store_dir = os.path.join(STORE_CACHE, now_date)
        if not os.path.exists(real_store_dir):  # dir is not exist, to make dir
            mk_dirs(real_store_dir)

        """ 加入try，防止存储失败 """
        try:
            file_name = getattr(file, 'filename')   # use getattr method to get file name
                                                    # from file object
            if is_md5_store_name:       # store name by md5
                _, store_name_md5 = filename2md5(file_name=file_name, _type='file')
                file_name = store_name_md5
            _real_file = os.path.join(real_store_dir, file_name)     # 文件真实存储
            """ 文件已存在，加上当前时间戳避免重复存在导致覆盖 """
            if os.path.exists(_real_file):
                file_names = os.path.splitext(file_name)
                suffix = (file_names[1]).lower() if len(file_names) > 1 else ''
                new_file_name = '%s-%s%s' % (file_names[0], get_now(format="%Y-%m-%d-%H-%M-%S"), suffix)
                _real_file = os.path.join(real_store_dir, new_file_name)
                file_name = new_file_name
            file.save(_real_file)       # save
            return True, {'name': file_name,
                          'md5': md5(file_name + get_now()),
                          'store_name': '%s/%s' % (now_date, file_name),
                          'path': os.path.join(real_store_dir, file_name),
                          'message': 'success'}
        except:
            return False, {'message': '文件存储Exception发生错误'}

    def _pdf2word(self, cmd5: str,
                  pdf_file: str, word_name: str,
                  start: int = None, end: int = None, pages: list = None,
                  *args, **kwargs):
        """
        pdf file convert to word file,
        buildin method
        the pdf file to transfer to word file format, have some parameters to execute,
        use multiprocess to achieve many file to convert,
        The number of multiple processes depends on the number of CPUs running the server/PC

        parameters detail:
        :param cmd5: the convert data md5
        :param pdf_file: the pdf file object (pdf file path)
        :param word_name: transfer to store word file name (word file name)
        :param start (int, optional): transfer file start page, default is 0
        :param end (int, optional): transfer file end page, default is max page
        :param pages (list, optional): transfer page list, such as: [1, 2, 5...]
        :param kwargs (dict, optional): Configuration parameters. Defaults to None.
        :return: json data
        use pdf file to transfer to word file
        some parameter is not must, use default

        data structure:
            {
                message: transfer result description,
                word_file: target file object, path + new file name
            }
        """
        # check pdf file
        if not pdf_file or not os.path.exists(pdf_file):
            return self.format_res(101, 'PDF文件不存在', {'md5': cmd5})
        if not os.path.isfile(pdf_file):
            return self.format_res(102, 'PDF文件不是一个正常PDF文件', {'md5': cmd5})
        pdf_path, pdf_name = os.path.split(pdf_file)
        pdf_names = os.path.splitext(pdf_name)
        if len(pdf_names) < 2 or pdf_names[1] not in self.DPF_EXTENSIONS:
            return self.format_res(103, 'PDF文件格式不正确', {'md5': cmd5})
        # check start page && end page
        if start and end and start > end:
            return self.format_res(104, '结束页不允许小于开始页', {'md5': cmd5})
        # check word file name
        if word_name:
            word_names = os.path.splitext(word_name)
            if len(word_names) < 2 or word_names[1] not in self.DOC_EXTENSIONS:
                word_name += self.default_doc_prefix
        else:
            word_name = pdf_names[0] + self.default_doc_prefix

        # 文件存储初始化
        now_date = get_now(format="%Y%m%d")
        real_store_dir = os.path.join(STORE_CACHE, now_date)
        if not os.path.exists(real_store_dir):  # dir is not exist, to make dir
            mk_dirs(real_store_dir)
        word_file = os.path.join(real_store_dir, word_name)  # 文件真实存储
        # check docx file is exist, exist is delete
        if os.path.exists(word_file):
            os.remove(word_file)

        # ---------------------------convert start--------------------------------------------------
        # convert pdf to docx
        cv = Converter(pdf_file)
        # all pages by default
        # cv.convert(docx_filename=word_file, start=start, end=end, pages=pages)

        # 通过参数使用调用不同的参数方法
        if pages:
            cv.convert(docx_filename=word_file, pages=pages)
        elif start and not end:
            cv.convert(docx_filename=word_file, start=start)
        elif not start and end:
            cv.convert(docx_filename=word_file, end=end)
        elif start and end:
            cv.convert(docx_filename=word_file, start=start, end=end)
        else:
            cv.convert(docx_filename=word_file)

        cv.close()
        # ---------------------------convert end--------------------------------------------------
        return self.format_res(100, 'success', {'md5': cmd5, 'word': word_file, 'name': word_name})

    def __pdf2word_no_multi_processing(self, pdf_list: dict):
        """
        pdf file convert to word file, not multiprocessing

        pdf_list data structure:
        {
            md5: {
                pdf: pdf file,
                word: word name,
                start: start page,
                end: end page,
                pages: page list
            },
            md5: {
                pdf: pdf file,
                word: word name,
                start: start page,
                end: end page,
                pages: page list
            }
            ...
        }

        return data structure:
        {
            status_id: int,
            message: str,
            data: list
        }
        """
        results = dict()
        """ 非多进程方式，循环处理 """
        for key, value in pdf_list.items():
            if not key or not value: continue
            # convert parameters deal
            start = int(value.get('start')) if value.get('start') else ''    # start page
            end = int(value.get('end')) if value.get('end') else ''     # end page
            if start and end and start > end:
                results[key] = {'ok': False, 'message': '结束页不允许小于开始页'}
                continue
            pages = value.get('pages') if value.get('pages') else []    # pages list
            # parameters initialize end
            _res = self._pdf2word(cmd5=key,
                                  pdf_file=value.get('pdf'), word_name=value.get('word'),
                                  start=start, end=end, pages=pages)
            _v = {
                'ok': True if _res.get('status_id') == 100 else False,
                'message': _res.get('message')
            }
            if _res.get('status_id') == 100:
                _v['word'] = _res.get('data').get('word')
                _v['name'] = _res.get('data').get('name')
            results[key] = _v
        # ===================== 转换完成 =====================
        for k, v in pdf_list.items():
            if not k or not v: continue
            _v = pdf_list.get(k)
            if k in results.keys():
                _v.update(results.get(k))
                pdf_list[k] = _v
        return self.format_res(100, 'success', pdf_list)

    def __pdf2word_by_multi_processing(self, pdf_list: dict):
        """
        pdf file convert to word file,
        by multiprocessing
        """
        results = list()
        # =========================== 多进程 start ===========================
        pool = multiprocessing.Pool(processes=self.cpu_count)
        for key, v in pdf_list.items():
            start = int(v.get('start')) if v.get('start') else ''    # start page
            end = int(v.get('end')) if v.get('end') else ''  # end page
            pages = v.get('pages') if v.get('pages') else []  # pages list
            # parameters initialize end
            results.append(pool.apply_async(func=self._pdf2word,
                                            args=(key, v.get('pdf'), v.get('word'), start, end, pages)))
        pool.close()
        pool.join()
        # =========================== 多进程 end ===========================
        for _r in results:
            _r_v = _r.get()
            if not _r: continue
            key = _r_v.get('data').get('md5')
            _d = {
                'ok': True if _r_v.get('status_id') == 100 else False,
                'message': _r_v.get('message')
            }
            if _r_v.get('status_id') == 100:
                _d['word'] = _r_v.get('data').get('word')
                _d['name'] = _r_v.get('data').get('name')
            if key in pdf_list.keys():
                _new_v = pdf_list.get(key)
                _new_v.update(_d)
                pdf_list[key] = _new_v
        return self.format_res(100, 'success', pdf_list)

    def pdf2word(self, pdf_list, is_multi_processing: bool = True):
        """
        PDF转WORD，基于pdf2docx实现
        批量转换采用多进程进行处理，也可以关闭多进程采用循环的方式进行转换，
        效率上多进程优高些
        多进程：__pdf2word_by_multi_processing
        非多进程：__pdf2word_no_multi_processing

        cpu count, default is pc/server cpu + 1
        :param is_multi_processing: is or not start work by multiprocess
        :param pdf_list: pdf file list
        return json data

        pdf_list data structure:
        {
            md5: {
                pdf: pdf file,
                word: word name,
                start: start page,
                end: end page,
                pages: page list
            },
            md5: {
                pdf: pdf file,
                word: word name,
                start: start page,
                end: end page,
                pages: page list
            }
            ...
        }

        return data structure:
        {
            status_id: int,
            message: str,
            data: list
        }
        """
        if not pdf_list:
            return self.format_res(101, '缺少pdf_list参数', [])
        # to execute convert method by is_multi_processing value
        return self.__pdf2word_by_multi_processing(pdf_list) if is_multi_processing \
            else self.__pdf2word_no_multi_processing(pdf_list)

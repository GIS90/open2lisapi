# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    the command execute ls、cd..

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/10/20 10:26 AM"
    __mail__ = "gaoming971366@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python subprocess_lib.py
# ------------------------------------------------------------
import sys
import os
import inspect
import types
from subprocess import PIPE, Popen


def get_cur_folder():
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(__file__))
    else:
        cur_folder = os.path.dirname(inspect.getfile(inspect.currentframe()))
        return os.path.abspath(cur_folder)


def _print_die(message):
    if not message:
        return
    print(message)


def _run_cmd(cmd, shell=True, check_exit_code=True, cwd=None):
    """
    execute command at shell
    :param cmd: command
    :param shell: is or not run shell mode
        if shell is True, command type is str
        else command type is list or tuple
    :param check_exit_code: check is or not return code
    :param cwd: current work dir
    :return: command return code, command content
    
    cmd:
      - "ls"
      - ["ls", "-a"]
    """
    if type(cmd) not in [types.StringType, types.ListType, types.TupleType]:
        return -1, 'Command type is error'

    if not cwd:
        cwd = get_cur_folder()

    if not shell:
        cmd = ' '.join(cmd)
    p = Popen(cmd,
              shell=True,
              bufsize=0,
              cwd=cwd,
              stdout=PIPE)
    output = p.communicate()[0]
    return_code = p.returncode
    if check_exit_code and return_code != 0:
        _print_die('Command "%s" failed.\n%s' % (' '.join(cmd), output))
    if return_code in [0, '0']:
        return_code = 0
    return return_code, output


def run_command(cmd, check_exit_code=True, shell=True, cwd=None):
    return _run_cmd(cmd, shell=shell, check_exit_code=check_exit_code, cwd=cwd)


def run_command_no_output(cmd, check_exit_code=True, shell=True, cwd=None):
    return _run_cmd(cmd, shell=shell, check_exit_code=check_exit_code, cwd=cwd)[0]


def check_command_by_which(cmd):
    return True if run_command_no_output("which %s" % cmd, check_exit_code=False) == 0 \
        else False

# -*- coding:utf-8 -*-

import os

def get_app_dir():
    return os.path.abspath(os.path.dirname(__file__))

def get_file_path(file_name):
    return os.path.join(get_app_dir(), file_name)

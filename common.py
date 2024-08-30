# -*- coding:utf-8 -*-

import os
import subprocess

def get_app_dir():
    return os.path.abspath(os.path.dirname(__file__))

def get_file_path(file_name):
    return os.path.join(get_app_dir(), file_name)

def get_script_path(script_name):
    return os.path.join(get_app_dir(), "scripts", script_name)

def run_script(file_name, *args):
    script = get_script_path(file_name)
    if not os.path.isfile(script):
        raise ValueError("Script %s not found" % script)
    return subprocess.check_call((script,) + args)
    
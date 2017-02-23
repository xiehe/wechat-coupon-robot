#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup
import py2exe
options = {"py2exe":{
    "compressed": 1, #压缩  
    "optimize": 2,
    "bundle_files": 1 #所有文件打包成一个exe文件  
}}
setup(
    # version = "0.3.9",
    # description = u"微信淘宝推广机器人",     
    # name = "run",
    # options = options,     
    # zipfile = None, # 不生成zip库文件 
    console = [{"script": "run.py", "icon_resources": [(1, "run.ico")] }]
)

# from glob import glob
# data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files (x86)\Common Files\Adobe\OOBE\PDApp\core\Microsoft.VC90.CRT\*.*'))]
# setup(
# data_files=data_files,
# console=[{"script": "run.py", "icon_resources": [(1, "run.ico")] }]
# )
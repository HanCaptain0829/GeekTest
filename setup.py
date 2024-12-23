# -*- coding: utf-8 -*-
from setuptools import setup

APP = ['Start.py']  # 要打包的主Python脚本列表
DATA_FILES = ['picture/*', 'log/GeekTest.log']  # 要包含的资源文件列表，使用通配符匹配images文件夹下的所有文件
OPTIONS = {
    'argv_emulation': True,  # 启用命令行参数模拟
    'packages': ['tkcalendar'],
    'iconfile': 'picture\\xmind.icns',  # 应用图标文件
    'plist': {  # 应用的plist配置信息
        'CFBundleName': 'GeekTest',
        'CFBundleDisplayName': 'GeekTest',
        'CFBundleVersion': '1.0.2',
        'CFBundleShortVersionString': '1.0.2',
        'CFBundleIdentifier': 'com.example.GeekTest',
        'NSHumanReadableCopyright': 'Copyright ? 2024 Geek. All rights reserved.',
    },
    # 'packages': ['data', 'gui','log','login','menu','gui\\testcase'],  #如果需要显式指定包，可以这样做（但通常不需要）
    # 'includes': ['CaseSql', 'InsertCaseSql','SqlConnect','LoginPage','MenuPage','UserinfoPage','LogConfig',
    #              'CheckCase','UserOption','XmindUploadCase','XmindUpdatePage'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],  # 打包时需要的额外依赖
)
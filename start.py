#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/20 下午9:14 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : start.py
# @desc : README.md

from configparser import ConfigParser
from os.path import isfile


def get_information_from_ini(items):
    """将ini文件内容转换为字典返回"""

    data = {}
    for key, value in items:
        data[key] = value

    return data


# 解析ini配置文件
try:
    config = ConfigParser()

    if isfile('config.ini'):

        config.read('config.ini')
        # 获取相关配置
        cloud = get_information_from_ini(config['cloud'].items())
        local = get_information_from_ini(config['local'].items())
        live2d = get_information_from_ini(config['live2d'].items())
        stt = get_information_from_ini(config['STT'].items())
        tts = get_information_from_ini(config['tts'].items())
        LAN_collaboration = get_information_from_ini(config['LAN collaboration'].items())

    # 配置文件缺失，还原文件
    else:
        # 云端大模型api
        config.add_section('cloud')
        config.set('cloud', 'AI_api', "")

        # 侧端AI接口， 默认ollama启动
        config.add_section('local')
        config.set('local', 'model_name', "llama3.1:latest")
        config.set('local', 'role', "user")
        config.set('local',
                   'character_setting',
                   """你叫mita，是一个语言简洁的辅助系统，当你收到需要编写代码的任务后，
                   你仅需使用纯文本的方式回答代码部分，其他省略""")

        # live2d模型配置
        config.add_section('live2d')
        config.set('live2d', 'path', r"米塔\\3.model3.json")

        # 语音转文字
        config.add_section('STT')

        # 文字转语音
        config.add_section("TTS")

        # 局域网内协作开发
        config.add_section('LAN collaboration')

        with open('config.ini', "w") as file:
            config.write(file)

except Exception as Error:
    print(Error)







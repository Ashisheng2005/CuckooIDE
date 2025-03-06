#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2025/1/18 下午5:53 
# @Author : Huzhaojun
# @Version：V 1.0
# @File : ErrorType.py
# @desc : README.md

class File(Exception):

    def __init__(self, *args, **kwargs):
        pass


class FilePathNotFind(File):

    def __init__(self, *args, **kwargs):
        pass


class Ollama_(Exception):

    def __init__(self, *args, **kwargs):
        pass


class ConnectError(Ollama_):

    def __init__(self, *args, **kwargs):
        pass

class ParametersNotFind(Exception):

    def __init__(self, *array, **keyword):
        pass
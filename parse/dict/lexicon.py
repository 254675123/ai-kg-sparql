#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

# 定义词典类
class Lexicon:
    "管理不同类型的词典"

    # 通用的词典
    lex_common = {}

    # 标点符号词典
    lex_sign = {}

    # 图谱词典
    lex_graph = {}

    def __init__(self):

        # 加载词典
        self.__load()

        return

    def __load(self):
        "加载各类型的词典"

        if len(self.lex_common) == 0:
            self.__load_common()

        if len(self.lex_sign) == 0:
            self.__load_sign()

        if len(self.lex_graph) == 0:
            self.__load_graph()

        return

    def __load_common(self):

        return

    def __load_sign(self):

        return

    def __load_graph(self):
        # 寻找词典文件
        dict_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lexicon_graph'))
        file_list = os.listdir(dict_dir)

        # 遍历文件
        for file_name in file_list:
            file_path = os.path.join(dict_dir, file_name)
            if os.path.isfile(file_path):
                f = open(file_path, 'r', encoding='UTF-8')
                lines = f.readlines()
                self.__append(file_name,lines)
                f.close()
        return

    def __append(self,file_name, lines):
        for line in lines:
            seg_list = line.strip().split()
            if len(seg_list) > 0:
                val = seg_list[0]
                # val加一个前缀
                val = "%s:%s" % (file_name, val)
                for index in range(1, len(seg_list)):
                    self.lex_graph[seg_list[index]] = val



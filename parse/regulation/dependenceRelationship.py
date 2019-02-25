#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from parse.regulation.syntacticNode import *

class DependenceRelationShip:
    "短语之间的依存关系"

    # 初始化
    def __init__(self):
        self.phrase_dict = {}

        self.phrase_list = []


    # 加载短语依存关系
    def load(self):
        file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), 'dependence_relationship'))
        if os.path.exists(file_name) == False:
            return self.phrase_dict

        f = open(file_name, 'r', encoding='UTF-8')
        lines = f.readlines()
        for line in lines:
            seg = line.strip().split(':')
            if len(seg) > 1:
                if seg[0] in self.phrase_dict.keys():
                    pass
                else:
                    self.phrase_dict[seg[0]] = seg[1]
        f.close()

        # 处理节点配对
        # 一个循环处理一条规则
        length = len(self.phrase_dict)
        for i in range(length):
            key = str(i)
            node_pair = SyntacticNodePair()
            node_pair.setValue(self.phrase_dict.get(key))
            self.phrase_list.append(node_pair)



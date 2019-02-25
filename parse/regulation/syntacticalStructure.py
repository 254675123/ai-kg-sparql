#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from parse.regulation.syntacticNode import SyntacticNode

class SyntacticalStructure:
    "语句的句式结构"

    # 初始化
    def __init__(self):
        self.syntactic_dict = {}


    # 加载句式规则
    def load(self):
        file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), 'syntactical_structure'))
        if os.path.exists(file_name) == False:
            return self.syntactic_dict

        f = open(file_name, 'r', encoding='UTF-8')
        lines = f.readlines()
        for line in lines:
            if line in self.syntactic_dict.keys():
                pass
            else:
                res = self.parseRuleExpression(line)
                self.syntactic_dict[line] = res

        f.close()

        return self.syntactic_dict

    # 解析句式规则
    def parseRuleExpression(self, rule):
        result = []
        segments = rule.strip().split('-')
        for val in segments:
            node = SyntacticNode()
            node.setValue(val)
            result.append(node)
        return result


#!/usr/bin/python
# -*- coding: UTF-8 -*-

from  parse.regulation.dependenceRelationship import DependenceRelationShip
from  parse.regulation.syntacticalStructure import SyntacticalStructure
from  parse.regulation.syntacticNode import *
from  parse.regulation.syntacticNode import *

# 句法规则管理类
class SyntacticalRule:
    "管理句法规则"

    # 句式规则
    dpd_rel = None

    # 短语依存关系
    syntatic_struct = None

    def __init__(self):
        ""
        if self.dpd_rel is None:
            self.dpd_rel = DependenceRelationShip()
            self.dpd_rel.load()

        if self.syntatic_struct is None:
            self.syntatic_struct = SyntacticalStructure()
            self.syntatic_struct.load()

    # 转换列表
    def convertNodeList(self, nodeList):
        n_node_list = []

        for node in nodeList:
            n_node = SyntacticNode()
            n_node.entity = node
            n_node.type = node.type

            n_node_list.append(n_node)

        return n_node_list

    # 使用语法规则进行合并
    def combineNode(self, o_nodeList):
        "按照依赖关系的优先级进行节点合并"
        nodeList = self.convertNodeList(o_nodeList)
        # 需要移除的序号列表
        rmList = []
        pre_node = None
        cur_node = None
        # 一个循环处理一条规则
        rule_list = self.dpd_rel.phrase_list
        for rule_pair in rule_list:
            length = len(nodeList)
            rmList.clear()
            # 单步长处理方法
            if rule_pair.step == '-':
                for i in range(length):
                    if (i == 0) :
                        pre_node = nodeList[0]
                        continue

                    cur_node = nodeList[i]

                    # 比较前一个节点和当前节点的类型是否与规则一致
                    if (rule_pair.pre_node.type == pre_node.type) and (rule_pair.cur_node.type == cur_node.type) :
                        # 检查方向
                        if rule_pair.direction == '>':
                            rmList.append(i-1)
                            cur_node.child_node = pre_node
                            pre_node = cur_node
                        elif  rule_pair.direction == '<':
                            rmList.append(i)
                            pre_node.child_node = cur_node

                    else:
                        pre_node = cur_node
                # 循环结束后，把合并的node移除去
                for x in rmList[::-1]:
                    del nodeList[x]

            # 多步长处理方法
            elif rule_pair.step == '--' and rule_pair.direction == '>':
                childnode = None
                for i in range(length):
                    cur_node = nodeList[i]
                    if cur_node.type == rule_pair.pre_node.type:
                        childnode = cur_node
                        break

                if childnode is None:
                    continue

                for i in range(length):
                    cur_node = nodeList[i]
                    if cur_node.type == rule_pair.cur_node.type:
                        cur_node.child_node = childnode

        return  nodeList

    # 检查是否符合句式规则
    def checkStatement(self, node_list):
        ""

        matched = True
        # 匹配到任何一个句式规则，则认为符合句式规则
        # 一个循环处理一条规则
        syntactic_dict = self.syntatic_struct.syntactic_dict
        for key in syntactic_dict.keys():
            rule_list = syntactic_dict.get(key)
            matched = True

            # 初始化索引位置
            rule_index = 0
            node_index = 0

            # 规则结束点为rule_index + 1 == len(rule_list)
            # 句子结束点为node_index + 1 == len(node_list)
            rule_length = len(rule_list)
            node_length = len(node_list)
            while (rule_index < rule_length and node_index < node_length):
                rule = rule_list[rule_index]
                node = node_list[node_index]

                # 两个节点类型相同，匹配
                if rule.type == node.type and rule.freq == '1':
                    rule_index += 1
                    node_index += 1
                    continue
                # 对于node节点存在相同的类型，需要进一步查看
                elif rule.type == node.type and rule.freq == 'n':
                    if (node_index + 1 < node_length):
                        next_node = node_list[node_index + 1]
                        if next_node.type == node.type:
                            node_index += 1
                        else:
                            rule_index += 1
                            node_index += 1
                    else:
                        rule_index += 1
                        node_index += 1

                # 两个节点类型不相同，不匹配
                else:
                    matched = False
                    break

            # 匹配成功
            if matched :
                break

        return matched

#!/usr/bin/python
# -*- coding: UTF-8 -*-



class SyntacticNode:
    "句法节点"

    def __init__(self):


        # 节点在句子中的类型
        self.type = None

        # 节点在句子中出现的频次
        self.freq = None

        # 子节点
        self.child_node = None

        # 在句子中的位序
        #self.position = None

        # 实体节点
        self.entity = None

    def setValue(self, val):
        ""
        segs = val.split(':')
        length = len(segs)
        if length > 1:
            self.type = segs[0]
            self.freq = segs[1]
        elif length == 1:
            self.type = segs[0]
            self.freq = "1"

class SyntacticNodePair:
    "节点依赖对"

    def __init__(self):
        self.pre_node = SyntacticNode()
        self.cur_node = SyntacticNode()
        # 记录依赖方向，'>'为正向，'<'逆向
        self.direction = None
        # 记录依赖步长，'-'为单步，'--'为多步
        self.step = None

    def setValue(self, val):
        ""
        # 正向单步依赖
        if val.find('->') > 0:
            self.direction = '>'
            self.step = '-'
            segs = val.split('->')
            self.pre_node.setValue(segs[0])
            self.cur_node.setValue(segs[1])

        # 正向多步依赖
        elif val.find('-->') > 0:
            self.direction = '>'
            self.step = '--'
            segs = val.split('-->')
            self.pre_node.setValue(segs[0])
            self.cur_node.setValue(segs[1])
        # 逆向单步依赖
        elif val.find('<-') > 0:
            self.direction = '<'
            self.step = '-'
            segs = val.split('<-')
            self.pre_node.setValue(segs[0])
            self.cur_node.setValue(segs[1])
        # 逆向多步依赖
        elif val.find('<--') > 0:
            self.direction = '<'
            self.step = '--'
            segs = val.split('<--')
            self.pre_node.setValue(segs[0])
            self.cur_node.setValue(segs[1])

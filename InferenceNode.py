#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 推理树节点
# 每个节点下面都可以关联多个边，每个边可以挂接多个节点
class InferenceNode:
    "记录节点和边"

    # 原始节点
    #orgin = None

    # 节点id 如Q31
    #id = None
    # type
    #type = None

    # 节点状态，已知状态还是未知状态
    # 已知状态时，该节点将作为条件
    #status = None

    # 节点之间的边，如P78
    # 字典的key为字符串，就是边的id；value为node的
    #claims = None
    # 请求的边
    #queryEdge = []

    def __init__(self):
        self.id = None
        self.name = None
        self.status = None
        self.queryEdge = []
        self.orgin = None
        self.type = None

    # 设置节点内容
    def setNodeValue(self, nodedata):
        "将取回来的实体节点赋值"

        # nodedata是一个字典型，只有一条数据
        for x in nodedata.keys():
            self.orgin = nodedata.get(x)
            self.id = x
            self.claims = self.orgin["claims"]
            self.type = self.orgin["type"]
            break;


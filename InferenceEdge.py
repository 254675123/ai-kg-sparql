#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 推理树节点与节点之间的边
# 每个节点下面都可以关联多个边，每个边可以挂接多个节点
class InferenceEdge:
    "记录边"

    # 边的id，如P78
    #id = None

    # type
    #type = None

    # 节点状态，已知状态还是未知状态
    # 已知状态时，该节点将作为条件
    #status = None

    #node list 节点列表
    #nodeList = []

    def __init__(self):
        # type 用于存储边的数据类型
        self.datatype = None
        # formula用于存储边下面的节点将要使用的公式
        self.formula = None
        # 边对应的节点，也可能没有
        self.nodeList = []
        self.id = None
        self.status = None


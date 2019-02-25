#!/usr/bin/python
# -*- coding: UTF-8 -*-

class SelectParam:
    'SPARQL 查询结果显示项'

    # 公共属性，一个列表项，默认为空列表
    #itemList = []

    def __init__(self):
        self.itemList = []

    # 组装列表中的结果项，形成如下结果
    # ?product ?type ?label 等
    def getSelectItem(self):
        "组装列表中的结果项"
        prefix = "select "

        for item in self.itemList:
            prefix += "?" + item
            prefix += " "
            #prefix += "?" + item + "Label"
            #prefix += " "

        return prefix;

# sp = SelectParam()
# sp.itemList.append("?product")
# sp.itemList.append("?type")

# str = sp.getSelectItem()
# print str;
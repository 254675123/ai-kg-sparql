#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ServiceParam
import  GroupParam
class WhereParam:
    'SPARQL 查询条件项'

    # 三元组列表
    # 公共属性，一个列表项，默认为空列表
    #itemList = []

    def __init__(self):
        self.itemList = []
        self.gp = GroupParam.GroupParam()

    # 组装列表中的结果项，形成如下结果
    # ?product ?type ?label 等
    def getSelectItem(self):
        "组装列表中的结果项"

        # return line
        nline = "\n"

        prefix = nline + "where " + nline
        prefix += "{" + nline

        for item in self.itemList:
            prefix += item + nline

        # 添加语种标签
        sp = ServiceParam.ServiceParam()
        prefix += sp.getLanguageLabel("zh-cn")
        prefix += nline
        prefix += "}" + nline

        # group部分 如果有统计函数，则需要加入分组
        flag = False
        if  flag:
            group = self.gp.getSelectItem()

            prefix += group

        return prefix;

    # 设置条件项
    #def setItemList(self, ):
# wp = WhereParam()
# wp.itemList.append("?product wdt:P98 ?o .")
# wp.itemList.append("?type wdt:P76 ?revenue .")

# str = wp.getSelectItem()
# print str;
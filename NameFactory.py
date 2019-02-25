#!/usr/bin/python
# -*- coding: UTF-8 -*-

class NameFactory:
    "生成名称"

    # 生成实体名称计数
    #entity_num = 0

    # 生成属性名称计数
    #property_num = 0

    def __init__(self):
        self.entity_num = 0
        self.property_num = 0

    def reset(self):
        self.entity_num = 0
        self.property_num = 0


    def getEntityName(self):
        self.entity_num += 1
        return  "entity%s" % (self.entity_num)


    def getPropertyName(self):
        self.property_num += 1
        return  "property%s" % (self.property_num)

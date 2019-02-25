#!/usr/bin/python
# -*- coding: UTF-8 -*-
import  NameFactory
import  SelectParam
import  WhereParam
from parse import *

# 定义分析自然语言次序，以生成sql语句
class NLAnalysisSql :
    "已经分好词的数组，分析其逻辑关系，以生成sql"
    def __init__(self):
        self.head_dict = {}

    # 创建Sparql语句
    def createSparql(self, data):
        "遍历数组数据"

        # 清空列表
        self.head_dict.clear()

        # 预处理一下分词结果项
        self.preprocess(data)

        # 生成命名未知实体和属性的对象
        nf = NameFactory.NameFactory()
        #nf.reset()

        sp = SelectParam.SelectParam()
        wp = WhereParam.WhereParam()

        # 第一个数据对象为实体
        length = len(data)
        pre_ent = None
        cur_ent = None
        for i in range(length):
            # 第一个节点是实体
            if i == 0:
                cur_ent = data[0]
                pre_ent = cur_ent

                # 如果长度为1，并且是一个主体
                if pre_ent.type == "subject":
                    temp_cur_pro = nf.getPropertyName()
                    temp_cur_ent = nf.getEntityName()
                    item = "wd:%s ?%s ?%s ." % (pre_ent.id, temp_cur_pro, temp_cur_ent)
                    sp.itemList.append(temp_cur_pro)
                    sp.itemList.append(temp_cur_ent)
                    sp.itemList.append(temp_cur_ent + "Label")
                    self.head_dict[temp_cur_pro] = cur_ent.text + "关系"
                    self.head_dict[temp_cur_ent] = cur_ent.text + "属性"
                    self.head_dict[temp_cur_ent + "Label"] = cur_ent.text + "属性名称"
                    wp.itemList.append(item)

                continue
            # 从第二个节点开始
            cur_ent = data[i]
            # 如果当前节点不是直接属性，则需要转换一个中间节点
            # 适用范围（腾讯的游戏有哪些产品，腾讯的桌面游戏有哪些）
            if (pre_ent.type == "subject" and cur_ent.type == "virtual_object"):
                temp_cur_pro = nf.getPropertyName()
                temp_cur_ent = nf.getEntityName()
                item = "wd:%s ?%s ?%s ." % (pre_ent.id, temp_cur_pro, temp_cur_ent)
                sp.itemList.append(temp_cur_ent)
                sp.itemList.append(temp_cur_ent + "Label")
                self.head_dict[temp_cur_ent] = cur_ent.text
                self.head_dict[temp_cur_ent + "Label"] = cur_ent.text + "名称"
                wp.itemList.append(item)

                temp_next_pro = nf.getPropertyName()
                #temp_next_ent = nf.getEntityName()
                item = "?%s ?%s wd:%s ." % (temp_cur_ent, temp_next_pro, cur_ent.id)
                wp.itemList.append(item)

                # 创建一个中间节点
                middle_ent = NLEntity(temp_cur_ent, "","unknown", "", "")
                middle_ent.name = temp_cur_ent
                middle_ent.text = cur_ent.text
                middle_ent.hiden_object_id = cur_ent.hiden_object_id
                pre_ent = middle_ent
            # 如果当前节点是直接属性，则直接拼接
            # 适用范围（腾讯和马化腾是啥关系等）
            elif (pre_ent.type == "subject" and cur_ent.type == "subject"):
                temp_cur_pro = nf.getPropertyName()
                temp_cur_ent = nf.getEntityName()
                cur_ent.name = temp_cur_ent
                item = "wd:%s ?%s wd:%s ." % (pre_ent.id, temp_cur_pro, cur_ent.id)
                sp.itemList.append(temp_cur_pro)
                sp.itemList.append(temp_cur_pro + "Label")
                self.head_dict[temp_cur_pro] = "联系"
                self.head_dict[temp_cur_pro + "Label"] = "联系" + "名称"
                wp.itemList.append(item)

                # 把当前节点给前一个节点
                pre_ent = cur_ent
            # 如果当前节点是直接属性，则直接拼接
            # 适用范围（腾讯的主营业务，腾讯的产品等）
            elif (pre_ent.type == "subject" and cur_ent.type == "indicators_object"):
                #temp_cur_pro = nf.getPropertyName()
                temp_cur_ent = nf.getEntityName()
                cur_ent.name = temp_cur_ent
                item = "wd:%s wdt:%s ?%s ." % (pre_ent.id, cur_ent.id, temp_cur_ent)
                sp.itemList.append(temp_cur_ent)
                sp.itemList.append(temp_cur_ent + "Label")
                self.head_dict[temp_cur_ent] = cur_ent.text
                self.head_dict[temp_cur_ent + "Label"] = cur_ent.text + "名称"
                wp.itemList.append(item)

                # 把当前节点给前一个节点
                pre_ent = cur_ent
            # 如果当前节点是直接属性，则直接拼接
            # 适用范围（腾讯的主营业务，腾讯的产品等）
            elif (pre_ent.type == "subject" and cur_ent.type == "indicators_number"):
                temp_cur_pro = nf.getPropertyName()
                temp_cur_ent = nf.getEntityName()
                cur_ent.name = temp_cur_ent
                item = "wd:%s wdt:%s ?%s ." % (pre_ent.id, cur_ent.id, temp_cur_ent)
                sp.itemList.append(temp_cur_ent)
                self.head_dict[temp_cur_ent] = cur_ent.text
                wp.itemList.append(item)
            # 如果当前节点是直接属性，则直接拼接
            # 适用范围（腾讯的主营业务，腾讯的产品等）
            elif (pre_ent.type == "subject" and cur_ent.type == "indicators_normal"):
                temp_cur_pro = nf.getPropertyName()
                temp_cur_ent = nf.getEntityName()
                cur_ent.name = temp_cur_ent
                item = "wd:%s wdt:%s ?%s ." % (pre_ent.id, cur_ent.id, temp_cur_ent)
                sp.itemList.append(temp_cur_ent)
                self.head_dict[temp_cur_ent] = cur_ent.text
                wp.itemList.append(item)
                # 把当前节点给前一个节点
                #pre_ent = cur_ent
            # 如果前一个节点是未知的，当前节点是直接属性，则直接拼接
            # 适用范围（腾讯游戏的竞品有哪些）
            elif (pre_ent.type == "unknown" and cur_ent.type == "indicators_object"):
                #temp_cur_pro = nf.getPropertyName()
                temp_cur_ent = nf.getEntityName()
                cur_ent.name = temp_cur_ent
                item = "?%s wdt:%s ?%s ." % (pre_ent.name, cur_ent.id, temp_cur_ent)
                sp.itemList.append(temp_cur_ent)
                sp.itemList.append(temp_cur_ent + "Label")
                self.head_dict[temp_cur_ent] = cur_ent.text
                self.head_dict[temp_cur_ent + "Label"] = cur_ent.text + "名称"
                wp.itemList.append(item)

                # 把当前节点给前一个节点
                pre_ent = cur_ent

            # 如果前一个节点是直接属性，当前是值，则直接拼接
            # 适用范围（腾讯游戏的营收怎么样）
            elif (pre_ent.type == "unknown" and cur_ent.type == "indicators_number"):
                # temp_cur_pro = nf.getPropertyName()
                temp_cur_ent = nf.getEntityName()
                cur_ent.name = temp_cur_ent
                item = "?%s wdt:%s ?%s ." % (pre_ent.name, cur_ent.id, temp_cur_ent)
                sp.itemList.append(temp_cur_ent)
                self.head_dict[temp_cur_ent] = cur_ent.text
                wp.itemList.append(item)

                # 把当前节点给前一个节点
                #pre_ent = cur_ent
            # 如果前一个节点是直接属性，当前是值，则直接拼接
            # 适用范围（腾讯游戏的营收怎么样）
            elif (pre_ent.type == "unknown" and cur_ent.type == "indicators_normal"):
                # temp_cur_pro = nf.getPropertyName()
                temp_cur_ent = nf.getEntityName()
                cur_ent.name = temp_cur_ent
                item = "?%s wdt:%s ?%s ." % (pre_ent.name, cur_ent.id, temp_cur_ent)
                sp.itemList.append(temp_cur_ent)
                self.head_dict[temp_cur_ent] = cur_ent.text
                wp.itemList.append(item)
            elif (pre_ent.type == "indicators_object" and cur_ent.type == "virtual_object"):
                temp_cur_pro = nf.getPropertyName()
                temp_cur_ent = nf.getEntityName()
                item = "?%s ?%s ?%s ." % (pre_ent.name, temp_cur_pro, temp_cur_ent)
                sp.itemList.append(temp_cur_ent)
                sp.itemList.append(temp_cur_ent + "Label")
                self.head_dict[temp_cur_ent] = cur_ent.text
                self.head_dict[temp_cur_ent + "Label"] = cur_ent.text + "名称"
                wp.itemList.append(item)

                temp_next_pro = nf.getPropertyName()
                #temp_next_ent = nf.getEntityName()
                item = "?%s ?%s wd:%s ." % (temp_cur_ent, temp_next_pro, cur_ent.id)
                wp.itemList.append(item)

                # 创建一个中间节点
                middle_ent = NLEntity(temp_cur_ent, "","unknown", "", "")
                middle_ent.name = temp_cur_ent
                middle_ent.text = cur_ent.text
                middle_ent.hiden_object_id = cur_ent.hiden_object_id
                pre_ent = middle_ent
            # 如果前一个节点是未知的，当前节点是直接属性，则直接拼接
            # 适用范围（腾讯游戏的产品的竞品有哪些）
            elif (pre_ent.type == "indicators_object" and cur_ent.type == "indicators_object"):
                # temp_cur_pro = nf.getPropertyName()
                temp_cur_ent = nf.getEntityName()
                cur_ent.name = temp_cur_ent
                item = "?%s wdt:%s ?%s ." % (pre_ent.name, cur_ent.id, temp_cur_ent)
                sp.itemList.append(temp_cur_ent)
                sp.itemList.append(temp_cur_ent + "Label")
                self.head_dict[temp_cur_ent] = cur_ent.text
                self.head_dict[temp_cur_ent + "Label"] = cur_ent.text + "名称"
                wp.itemList.append(item)

                # 把当前节点给前一个节点
                pre_ent = cur_ent
            # 如果前一个节点是未知的，当前节点是直接属性，则直接拼接
            # 适用范围（腾讯游戏产品营收怎么样）
            elif (pre_ent.type == "indicators_object" and cur_ent.type == "indicators_number"):
                # temp_cur_pro = nf.getPropertyName()
                temp_cur_ent = nf.getEntityName()
                cur_ent.name = temp_cur_ent
                item = "?%s wdt:%s ?%s ." % (pre_ent.name, cur_ent.id, temp_cur_ent)
                sp.itemList.append(temp_cur_ent)
                self.head_dict[temp_cur_ent] = cur_ent.text
                wp.itemList.append(item)

                # 把当前节点给前一个节点
                # 如果 当前节点类型为number，则不用把当前节点作为前一个节点pre_ent = cur_ent
            # 如果前一个节点是未知的，当前节点是直接属性，则直接拼接
            # 适用范围（腾讯游戏产品营收怎么样）
            elif (pre_ent.type == "indicators_object" and cur_ent.type == "indicators_normal"):
                # temp_cur_pro = nf.getPropertyName()
                temp_cur_ent = nf.getEntityName()
                cur_ent.name = temp_cur_ent
                item = "?%s wdt:%s ?%s ." % (pre_ent.name, cur_ent.id, temp_cur_ent)
                sp.itemList.append(temp_cur_ent)
                self.head_dict[temp_cur_ent] = cur_ent.text
                wp.itemList.append(item)


        sql = sp.getSelectItem()
        sql += wp.getSelectItem()

        return sql


    # 对自然语言处理结果的预处理
    def preprocess(self, data):
        "预处理"
        length = len(data)
        pre_ent = None
        cur_ent = None
        position = 0
        for i in range(length):
            if i == 0:
                cur_ent = data[0]
                pre_ent = cur_ent
                continue

            cur_ent = data[i]
            if pre_ent.type == "indicators_number" and cur_ent.type == "formula":
                position = i
                pre_ent.formula = cur_ent.dict_text
                break
            else:
                pre_ent = cur_ent

        if position != 0:
            del data[position]

    # 对自然语言处理结果返回项的预处理（适合json格式）
    def jsonprocess(self, data):
        "预处理"

        wordDict = []
        length = len(data)
        for i in range(length):
            cur_ent = data[i]
            wordDict.append(cur_ent.getJson())
        return wordDict


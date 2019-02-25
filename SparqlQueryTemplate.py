#!/usr/bin/python
# -*- coding: UTF-8 -*-

import SelectParam
import  WhereParam
import  InferenceTree
import  InferenceNode
import  InferenceEdge
import  InferenceSql

# 负责组装不同部分
class SparqlQueryTemplate:
    'SPARQL 查询模板'

    # 生成Sparql语句
    def getQuerySql(self, itemList, flag):
        "获取查询Sparql语句"

        # return line
        nline = "\n"
        # select部分
        sp = SelectParam.SelectParam()
        select = sp.getSelectItem()

        # where部分
        wp = WhereParam.WhereParam()
        where = wp.getSelectItem()

        # 如果需要子查询, flag==1, 需要迭代执行
        sqt = ""
        if flag == 1:
            # flag = xx(itemList)
            sqt = SparqlQueryTemplate.getQuerySql(itemList, 0)
            sqt = "{ %s }" % (sqt)

        # 把所有的连接在一起
        result = select + nline
        result += where + nline
        if sqt != "":
            result += sqt + nline


    # 接收传入数据
    def receiveInputData(self, data, testflag):
        "接收处理数据按步骤处理数据"

        # 查询实体和属性对象
        query_data = self.queryData(data)

        # 比较实体中的属性是否全部包含条件属性（文中给出的属性）
        # 同时创建推理树InferenceTree
        inf_tree = self.createInferenceTree(query_data, testflag)

        # 根据推理树生成sql语句
        sparql = self.createSparqlStatement(inf_tree)

        print(sparql)

        # 执行语句
        #result = Wikiapi.getQueryDataBySparql(sparql)

        #print(result)

        return sparql




    # 根据传入的数据，查询相应的实体和属性
    def queryData(self, data):
        # 第一步，获取实体列表、属性列表和其他列表
        entityList = data["subject"]
        propertyList = data["indicator"]
        otherList = data["formula"]

        # 遍历实体名称列表，,找寻图谱中对应的实体
        qList = []  # 定义一个空列表，保存图谱中的节点
        for entName in entityList:
            # 请求api，获取对应的节点实体
            qentityId = Wikiapi.getwbsearchentitiesByName(entName)
            if qentityId is not None:
                qList.append(qentityId)

        # 遍历属性，获取属性对象
        pList = []  # 定义一个空列表，保存图谱中的属性（边）
        for proName in propertyList:
            # 获取边的定义
            pproperId = Wikiapi.getwbsearchepropertiesByName(proName)
            if pproperId is not None:
                pList.append(pproperId)

        # 将查询结果返回
        result_data = {"entity": qList, "property": pList}
        return result_data

    # 创建推理树
    def createInferenceTree(self, query_data, testflag):
        "根据查询结果生成推理树, 当前仅为一级推理树，需要扩展成多级 推理树"

        # 取出实体和属性
        qList = query_data["entity"]
        pList = query_data["property"]

        # 定义对应的字典
        q_dict = {}
        p_dict = {}
        # 定义一颗推理树
        infTree = InferenceTree.InferenceTree()

        # 取出实体节点，作为根节点(只取一个作为根节点)
        root_node = InferenceNode.InferenceNode()
        infTree.root = root_node

        # 遍历收到的所有实体
        for ent_id in qList:
            entity = Wikiapi.getwbentitiesByid(ent_id)
            q_dict[ent_id] = entity


        # 第一个节点作为根节点
        if len(qList) > 0:
            first_id = qList[0]
            root_entity = q_dict.get(first_id)
            root_node.setNodeValue(root_entity)
            root_node.status = "known"
            # 已经处理的节点，从字典中移除
            del q_dict[first_id]

        # 遍历所有边，是否在当前节点的声明中
        cur_node = root_node
        # 定义未发现的边
        #unknowPropertyList = []
        for pro in pList:
            flag = self.entityContainsProperty(cur_node.claims, pro)
            if flag:
                # 保存推理树边信息
                edge = InferenceEdge.InferenceEdge()
                edge.status = "known"
                edge.id = pro
                cur_node.queryEdge.append(edge)
            else:
                # 为多级推理树做准备
                p_dict[pro] = None
                #continue
                #unknowPropertyList.append(pro)

        # 如果q_dict,p_dict是空的，则所有属性已经匹配，不需要再进行多级节点推理

        # 如果q_dict,p_dict不为空，则仍然存在属性，在后续节点中，需要进行多级推理
        # 以根节点作为初始节点，向后遍历，参数为未发现的实体列表和属性
        if testflag == 1:
            if (len(q_dict) > 0 or len(p_dict) > 0) :
               self.iterateNodeofEdge(cur_node, q_dict, p_dict, 1)

        return infTree

    # 定义判断函数，一个实体是否包含给定的属性
    def entityContainsProperty(self, claims, property):
        # 是否存在该键
        hasKey = False
        # 声明是一个字典结构
        # 如果字典中的数量大于0，则说明其中有属性
        if len(claims) == 0 :
            return False

        # 匹配属性
        # 检查是否存在该key
        if property in claims.keys():
            hasKey = True

        return hasKey
    # 从实体中获取边对应的节点列表
    def getPropertyEndNodeFromEntity(self, cur_node, property):

        # 声明是一个字典结构
        claims = cur_node.claims
        # 如果字典中的数量大于0，则说明其中有属性
        if len(claims) == 0 :
            return

        # 检查是否存在该key
        qidList = []
        if property in claims.keys():
            resultList = claims.get(property)
            for x in resultList :
                mainsnakdict = x["mainsnak"]
                datatype = mainsnakdict["datatype"]
                if datatype == "wikibase-item":
                    datavaluedict = mainsnakdict["datavalue"]
                    valuedict = datavaluedict["value"]
                    qidList .append(valuedict["id"])

        return qidList


    # 根据推理树生成sql语句
    def createSparqlStatement(self, inftree):
        "根据推理树生成sql语句"

        # 定义推理sql对象
        isql = InferenceSql.InferenceSql()
        sql = isql.createSparqlStatement(inftree)

        # for x in root_node.queryEdge:
        #     sp.itemList.append("result"+x.id)
        #
        # # 条件项
        # for y in root_node.queryEdge:
        #     temp = "wd:%s wdt:%s ?%s ." % (root_node.id, y.id, "result"+y.id)
        #     wp.itemList.append(temp)


        print(sql)

        return  sql


    # 遍历图谱节点的边，寻找已知节点和属性
    def iterateNodeofEdge(self, cur_node, q_dict, p_dict, depth):
        "cur_node 为当前推理树节点"
        "q_dict 为未知的实体节点"
        "p_dict 为未知的属性边"

        # 遍历深度大于2时，结束
        if depth >2 :
            return

        # 从当前节点的边中，开始找下一级节点
        # 然后按照节点id，查询实体详细信息

        # 如果当前节点的边不为空，则先按照当前节点的边查找
        if len(cur_node.queryEdge) > 0:
            matchList = []
            qidList = None
            for edge in cur_node.queryEdge:
                # 如果边和节点已经匹配完，则不需要再查找
                # 清空列表
                matchList.clear()
                # 根据属性，找到属性挂接的节点
                qidList = self.getPropertyEndNodeFromEntity(cur_node, edge.id)
                if len(q_dict) == 0:
                    break

                # 检查结果节点是否有已知的节点
                for give in q_dict:
                    if give in qidList:
                        # 将该节点加入到该边中
                        n_node = InferenceNode.InferenceNode()
                        n_node.id = give
                        edge.nodeList.append(n_node)
                        # 加入匹配列表
                        matchList.append(give)
                # 删除匹配的id
                for x in matchList:
                    del q_dict[x]

            # 如果q_dict仍然不为空，则需要进一步迭代
            if (len(q_dict) > 0 or len(p_dict) > 0 ):
                self.iterateEdgeofNode(edge, qidList, q_dict, p_dict, depth+1)
        # 如果节点的边为空，遍历当前节点的每条边
        # 如果当前节点的claims为空，则跳过该节点
        if cur_node.claims is None:
            return None
        # 如果边和节点仍然没有匹配完
        if (len(q_dict) > 0):
            # 遍历当前节点的所有claims
            matchList = []
            for property in cur_node.claims.keys():
                if (len(q_dict) == 0):
                    break
                # 清空列表
                matchList.clear()
                # 根据属性，找到属性挂接的节点
                temp_qidList = self.getPropertyEndNodeFromEntity(cur_node, property)
                if len(temp_qidList) == 0:
                    continue
                # 检查结果节点是否有已知的节点
                for give in q_dict:
                    if give in temp_qidList:
                        # 将该节点加入到该边中
                        n_node = InferenceNode.InferenceNode()
                        n_node.id = give
                        edge.nodeList.append(n_node)
                        # 加入匹配列表
                        matchList.append(give)
                # 删除匹配的id
                for x in matchList:
                    del q_dict[x]



    # 遍历图谱结构，寻找已知节点和属性
    def iterateEdgeofNode(self, edge, qidList, q_dict, p_dict, depth):
        "cur_node 为当前推理树节点, qidList为下一个迭代节点的候选实体列表"
        "q_dict 为未知的实体节点"
        "p_dict 为未知的属性边"

        # 遍历深度大于2时，结束
        if depth >2 :
            return

        # 如果qidList 的列表没有值，则返回
        if len(qidList) == 0 :
            return None
        # 创建中间节点
        cur_node = InferenceNode.InferenceNode()
        cur_node.status = "unknown"
        edge.nodeList.append(cur_node)

        # 遍历收到的所有实体
        candidate_entity = None
        matchList = []
        for ent_id in qidList:
            if (len(q_dict) == 0 and len(p_dict) == 0):
                return
            # 还有没有匹配到的
            candidate_entity = Wikiapi.getwbentitiesByid(ent_id)
            n_node = InferenceNode.InferenceNode()
            n_node.setNodeValue(candidate_entity)
            n_node.status = "unknown"
            # 查找边是否在该实体中
            matchList.clear()
            for pro in p_dict.keys():
                flag = self.entityContainsProperty(n_node.claims, pro)
                if flag:
                    # 保存推理树边信息
                    n_edge = InferenceEdge.InferenceEdge()
                    n_edge.status = "known"
                    n_edge.id = pro
                    cur_node.queryEdge.append(n_edge)
                    matchList.append(pro)
                else:
                    # 为多级推理树做准备
                    #p_dict[pro] = None
                    continue
            # 删除匹配的id
            for x in matchList:
                del p_dict[x]

            # 遍历所有的节点边，看是否边的另一头存在所需要的实体
            # 如果节点的边为空，遍历当前节点的每条边
            # 如果当前节点的claims为空，则跳过该节点
            if n_node.claims is None:
                return None
            # 如果边和节点仍然没有匹配完
            if (len(q_dict) > 0):
                matchList = []
                # 遍历当前节点的所有claims
                for property in n_node.claims.keys():
                    if (len(q_dict) == 0):
                        break
                    # 清空列表
                    matchList.clear()
                    # 根据属性，找到属性挂接的节点
                    temp_qidList = self.getPropertyEndNodeFromEntity(n_node, property)
                    if len(temp_qidList) == 0:
                        continue
                    # 检查结果节点是否有已知的节点
                    for give in q_dict:
                        if give in temp_qidList:
                            # 保存推理树边信息
                            temp_edge = InferenceEdge.InferenceEdge()
                            temp_edge.status = "known"
                            temp_edge.id = property
                            cur_node.queryEdge.append(temp_edge)

                            # 将该节点加入到该边中
                            temp_node = InferenceNode.InferenceNode()
                            temp_node.id = give
                            temp_node.status = "known"
                            temp_edge.nodeList.append(temp_node)
                            # 加入匹配列表
                            matchList.append(give)
                    # 删除匹配的id
                    for x in matchList:
                        del q_dict[x]



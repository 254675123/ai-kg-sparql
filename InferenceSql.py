#!/usr/bin/python
# -*- coding: UTF-8 -*-
import  SelectParam
import  WhereParam


# 推理查询语句
# 根据推理树的节点和边，选择出需要的结果项和条件项
class InferenceSql:
    "推理节点和边"

    def __init__(self):
        self.iid = None


    # 根据推理树生成sql语句
    def createSparqlStatement(self, inftree):
        "根据推理树生成sql语句"

        # 判断推理树中是否包含统计边
        if self.containsStatisticEdge(inftree.root):
            dd = None

        # 获取根节点
        root_node = inftree.root
        # 创建selectParam对象
        # 把推理树节点的所有边，放在结果项中
        sp = SelectParam.SelectParam()
        # 拿到实体节点
        wp = WhereParam.WhereParam()

        # 遍历所有树节点
        self.ergodicInferenceTree(root_node, None, sp, wp)

        sql = sp.getSelectItem()
        sql += wp.getSelectItem()

        return sql

    # 定义遍历推理树，查找未知节点和已知节点
    def ergodicInferenceTree(self, root_node, root_node_edge, sp, wp):
        "遍历推理树, 根节点为root_node, 将结果项放入sp中, 条件项放入wp中"
        if root_node is None :
            return

        # 当前节点没有边了，则结束
        cur_node = root_node
        if len(cur_node.queryEdge) > 0:

            # 如果当前节点状态为unknown，则放入结果项中
            if cur_node.status == "unknown" and root_node_edge is not None:
                sp.itemList.append(cur_node.name)

            # 取边
            cur_edges = cur_node.queryEdge
            # 每一条边产生一个条件三元组
            for edge in cur_edges :
                nodeList = edge.nodeList
                # 没有节点，不考虑
                if len(nodeList) == 0 :
                    sp.itemList.append("result" + edge.id)
                    if cur_node.status == "unknown":
                        triple = "?%s wdt:%s ?%s ." % (cur_node.name, edge.id, "result" + edge.id)
                        wp.itemList.append(triple)
                    else:
                        triple = "wd:%s wdt:%s ?%s ." % (cur_node.id, edge.id, "result" + edge.id)
                        wp.itemList.append(triple)
                    continue

                # 存在节点，取出第一个节点
                temp_node = nodeList[0]
                if temp_node.status == "unknown":
                    temp_node.name = "result"+edge.id
                    if cur_node.status == "unknown":
                        triple = "?%s wdt:%s ?%s ." % (cur_node.id, edge.id, temp_node.name)
                        wp.itemList.append(triple)
                    else:
                        triple = "wd:%s wdt:%s ?%s ." % (cur_node.id, edge.id, temp_node.name)
                        wp.itemList.append(triple)

                elif cur_node.status == "unknown":
                    triple = "?%s wdt:%s wd:%s ." % (cur_node.name, edge.id, temp_node.id)
                    wp.itemList.append(triple)
                else:
                    triple = "wd:%s wdt:%s wd:%s ." % (cur_node.id, edge.id, temp_node.id)
                    wp.itemList.append(triple)
                # 迭代节点
                self.ergodicInferenceTree(temp_node,edge, sp, wp)

    # 检查推理树中是否有统计边
    def containsStatisticEdge(self, root_node):
        "检查边中是否有formula"
        if root_node is None :
            return False

        result = False
        for edge in root_node.queryEdge :
            if edge.formula is not None:
                result = True
                break
            elif len(edge.nodeList) > 0:
                result = self.containsStatisticEdge(edge.nodeList[0])
                if result :
                    break
        return  result

        # 定义遍历推理树，查找未知节点和已知节点
        def ergodicInferenceTreeForStatics(self, root_node, root_node_edge, sp, wp):
            "遍历推理树, 根节点为root_node, 将结果项放入sp中, 条件项放入wp中"
            if root_node is None:
                return

            # 当前节点没有边了，则结束
            cur_node = root_node
            if len(cur_node.queryEdge) > 0:

                # 如果当前节点状态为unknown，则放入结果项中
                if cur_node.status == "unknown" and root_node_edge is not None:
                    sp.itemList.append(cur_node.name)

                # 取边
                cur_edges = cur_node.queryEdge
                # 每一条边产生一个条件三元组
                for edge in cur_edges:
                    nodeList = edge.nodeList
                    # 判断边是分组边（仅有P75和P81为分组边）
                    if edge.id == "P75":
                        wp.gp.itemList

                    # 没有节点，不考虑
                    if len(nodeList) == 0:
                        sp.itemList.append("result" + edge.id)
                        if cur_node.status == "unknown":
                            triple = "?%s wdt:%s ?%s ." % (cur_node.name, edge.id, "result" + edge.id)
                            wp.itemList.append(triple)
                        else:
                            triple = "wd:%s wdt:%s ?%s ." % (cur_node.id, edge.id, "result" + edge.id)
                            wp.itemList.append(triple)
                        continue

                    # 存在节点，取出第一个节点
                    temp_node = nodeList[0]
                    if temp_node.status == "unknown":
                        temp_node.name = "result" + edge.id
                        if cur_node.status == "unknown":
                            triple = "?%s wdt:%s ?%s ." % (cur_node.id, edge.id, temp_node.name)
                            wp.itemList.append(triple)
                        else:
                            triple = "wd:%s wdt:%s ?%s ." % (cur_node.id, edge.id, temp_node.name)
                            wp.itemList.append(triple)

                    elif cur_node.status == "unknown":
                        triple = "?%s wdt:%s wd:%s ." % (cur_node.name, edge.id, temp_node.id)
                        wp.itemList.append(triple)
                    else:
                        triple = "wd:%s wdt:%s wd:%s ." % (cur_node.id, edge.id, temp_node.id)
                        wp.itemList.append(triple)
                    # 迭代节点
                    self.ergodicInferenceTree(temp_node, edge, sp, wp)
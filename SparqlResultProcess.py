#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys


class SparqlResultProcess:
    "对请求的结果进行进一步处理"

    # 处理显示头
    def processHeads(self, head, result):

        if result is None:
            return result
        # 处理头
        head_data = result["head"]
        head_items = head_data["vars"]
        length = len(head_items)
        for i in range(length):
            head_name = head_items[i]
            if head_name in head.keys():
                head_items[i] = head.get(head_name)

        # 处理数据
        res_data = result["results"]
        res_bindings = res_data["bindings"]
        length = len(res_bindings)
        for i in range(length):
            res_item = res_bindings[i]
            # 添加项
            for key in head.keys():
                if key in res_item.keys():
                    n_key = head.get(key)
                    n_key_val = res_item.get(key)
                    res_item[n_key] = n_key_val
            # 移除项
            for key in head.keys():
                if key in res_item.keys():
                    del res_item[key]

        return  result

    # 处理查询结果
    def processResult(self, data, result):
        "按照data中的函数，对result进行处理"

        # 从data中查找函数名称
        res_ent = self.getFunctionName(data)
        if res_ent is None:
            return result

        # 获取结果数据列表
        heads = result["head"]
        bindings = result["results"]
        bindings_list = bindings["bindings"]
        # 按照函数执行
        if res_ent.formula == "max":
            self._matchMax(bindings_list,res_ent.name)
        elif res_ent.formula == "min":
            self._matchMin(bindings_list, res_ent.name)
        elif res_ent.formula == "avg":
            self._matchAvg(bindings_list, heads, res_ent.name)
        elif res_ent.formula == "sum":
            self._matchSum(bindings_list, heads, res_ent.name)
        return  result

    # 获取函数名称
    def getFunctionName(self, data):
        "从data中抽取函数名称"
        res_ent = None
        for ent in data:
            if (ent.type == "indicators_number" and ent.formula is not None):
                res_ent = ent
                break

        return res_ent

    # 处理最大值
    def _matchMax(self, bindings, name):
        "寻找最大的项"
        if len(bindings) == 0:
            return None
        max_value = float('-inf')
        max_item = None
        for item in bindings:
            col_val = item[name]
            val = col_val["value"]
            temp_val = float(val)

            if temp_val > max_value:
                max_value = temp_val
                max_item = item

        bindings.clear()
        bindings.append(max_item)

    # 处理最小值
    def _matchMin(self, bindings, name):
        "寻找最小的项"
        if len(bindings) == 0:
            return None
        min_value = float('inf')
        min_item = None
        for item in bindings:
            col_val = item[name]
            val = col_val["value"]
            temp_val = float(val)

            if temp_val < min_value:
                min_value = temp_val
                min_item = item

        bindings.clear()
        bindings.append(min_item)


    # 处理平均值
    def _matchAvg(self, bindings, head,name):
        "统计平均值"
        if len(bindings) == 0:
            return None
        avg_value = float(0.0)
        length = len(bindings)
        temp_item = None
        for item in bindings:
            col_val = item[name]
            val = col_val["value"]
            avg_value += float(val)
            temp_item = item


        bindings.clear()
        vars = head["vars"]
        vars.clear()
        vars.append("avg")
        avg_value /= length
        data_val = {"value": avg_value}
        data = {"avg": data_val}
        bindings.append(data)
        #bindings.append(min_item)

    # 统计总和
    def _matchSum(self, bindings, head,name):
        "统计总和"
        if len(bindings) == 0:
            return None
        sum_value = float(0.0)
        #length = len(bindings)
        temp_item = None
        for item in bindings:
            col_val = item[name]
            val = col_val["value"]
            sum_value += float(val)
            temp_item = item

        bindings.clear()
        vars = head["vars"]
        vars.clear()
        vars.append("sum")
        data_val = {"value": str(sum_value)}
        data = {"sum": data_val}
        bindings.append(data)
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import urllib
import urllib.request
import urllib.parse


_HOST = 'http://120.26.58.228/w/api.php'

class Wikiapi:
    "访问wikiapi"

    # 全局Wikidata服务地址
    #_HOST = 'http://120.26.58.228/w/api.php'


    # 通过关键词搜索实体
    # 注意：该关键词仅匹配开头位置
    def getwbsearchentitiesByName(self, item_name):
        # 设置要搜索的数据
        body_value = {"search": item_name, "language": "zh"}
        body_value_encode = urllib.parse.urlencode(body_value).encode('utf8')
        # 设置action
        action = {"action": "wbsearchentities", "format": "json"}
        action_encode = urllib.parse.urlencode(action)

        # 定义请求
        request = urllib.request.Request(url=_HOST + '?' + action_encode, data=body_value_encode)
        print(request)
        res_data = urllib.request.urlopen(request)
        res = res_data.read()
        # 解码数据，并返回json对象
        result = res.decode()
        result = json.loads(result)
        success = result["success"]
        if success != 1:
            return
        # 获取搜索结果，结果是数组型
        search_result = result["search"]
        if len(search_result) > 0:
            # 实体id，如Q31
            for x in search_result:
                if x["label"] == item_name :
                    return x["id"]

            return
        else:
            return

    # 通过关键词搜索属性
    # 注意：该关键词仅匹配开头位置
    def getwbsearchepropertiesByName(self, item_name):
        # 设置要搜索的数据
        body_value = {"search": item_name, "language": "zh"}
        body_value_encode = urllib.parse.urlencode(body_value).encode('utf8')
        # 设置action
        action = {"action": "wbsearchentities", "type":"property", "format": "json"}
        action_encode = urllib.parse.urlencode(action)
        # 定义请求
        request = urllib.request.Request(url=_HOST + '?' + action_encode, data=body_value_encode)

        res_data = urllib.request.urlopen(request)
        res = res_data.read()

        # 解码数据，并返回json对象
        result = res.decode()
        result = json.loads(result)
        success = result["success"]
        if success != 1:
            return None
        # 获取搜索结果，结果是数组型
        search_result = result["search"]
        if len(search_result) > 0:
            # 实体id，如Q31
            for x in search_result:
                if x["label"] == item_name :
                    return x["id"]

            return search_result
        else:
            return None

    # 通过实体id搜索实体
    # 注意：搜索结果包含实体节点本身和所有关系声明
    def getwbentitiesByid(self, ent_id):
        body_value = {"search": ent_id, "language": "zh"}
        body_value_encode = urllib.parse.urlencode(body_value).encode('utf8')
        action = {"action": "wbgetentities", "ids": ent_id, "format": "json"}
        action_encode = urllib.parse.urlencode(action)

        request = urllib.request.Request(url=_HOST + '?' + action_encode, data=body_value_encode)

        res_data = urllib.request.urlopen(request)
        res = res_data.read()

        result = res.decode()
        result = json.loads(result)

        success = result["success"]
        if success != 1:
            return None
        # 获取搜索结果，结果是数组型
        search_result = result["entities"]
        if len(search_result) > 0:
            return search_result
        else:
            return None




    # 通过实体id搜索属性
    # 注意：搜索结果包含实体节点的所有关系声明
    def getwbclaimsByEntity(self, entity_id):
        body_value = {"search": entity_id, "language": "zh"}
        body_value_encode = urllib.parse.urlencode(body_value).encode('utf8')
        action = {"action": "wbgetclaims", "entity" : entity_id ,"format": "json"}
        action_encode = urllib.parse.urlencode(action)

        request = urllib.request.Request(url=_HOST + '?' + action_encode, data=body_value_encode)

        res_data = urllib.request.urlopen(request)
        res = res_data.read()

        result = res.decode()
        result = json.loads(result)
        return result


    # 通过sql获取查询结果
    def getQueryDataBySparql(self, sparql):
        "执行Sparql语句"

        # 主机服务地址
        host = "http://120.26.58.228/sparql"
        querystr = urllib.parse.quote(sparql)
        url = host + '?query=' + querystr

        request = urllib.request.Request(url)
        request.add_header('Accept', 'application/sparql-results+json')

        try:
            res_data = urllib.request.urlopen(request)
            result = res_data.read()
        except urllib.error.HTTPError:
            print("exception!")

        #print("query result: %s" % (result))

        result = result.decode()
        result = json.loads(result)
        return result





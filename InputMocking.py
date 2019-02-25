#!/usr/bin/python
# -*- coding: UTF-8 -*-
import SparqlQueryTemplate
import NLEntity
import  NLAnalysisSql

import  Wikiapi
import  SparqlResultProcess

# 模拟输入数据
class InputMocking:
    "mocking data"



    entityList = ["深圳市腾讯计算机系统有限公司"]
    properList = ["产品","产品营收"]
    #properList = []
    #properList = ["主营业务"]
    otherList = ["最大"]

    dict = {"subject":entityList, "indicator":properList, "formula":otherList}

    #sqt = SparqlQueryTemplate.SparqlQueryTemplate()
    #sqt.receiveInputData(dict,1)



    test_data = []
    # # 腾讯的游戏有哪些
    # obj1 = NLEntity.NLEntity("腾讯","subject","Q42857")
    # obj2 = NLEntity.NLEntity("游戏","virtual_object","Q43076")
    # test_data.append(obj1)
    # test_data.append(obj2)

    # # 腾讯的主营业务有哪些
    # obj1 = NLEntity.NLEntity("腾讯", "subject", "Q42857")
    # obj2 = NLEntity.NLEntity("主营业务", "indicators_object", "P77")
    # test_data.append(obj1)
    # test_data.append(obj2)

    # # 腾讯产品的营收有哪些
    # obj1 = NLEntity.NLEntity("腾讯", "subject", "Q42857")
    # obj2 = NLEntity.NLEntity("产品", "indicators_object", "P76")
    # obj21 = NLEntity.NLEntity("竞品", "indicators_object", "P80")
    # obj3 = NLEntity.NLEntity("营收", "indicators_number", "P78")
    # test_data.append(obj1)
    # test_data.append(obj2)
    # test_data.append(obj21)
    # test_data.append(obj3)

    # 腾讯产品的营收有哪些
    obj1 = NLEntity.NLEntity("腾讯", "subject", "Q42857")
    obj2 = NLEntity.NLEntity("产品", "indicators_object", "P76")
    obj3 = NLEntity.NLEntity("营收", "indicators_number", "P78")
    obj3.formula = "max"
    test_data.append(obj1)
    test_data.append(obj2)
    test_data.append(obj3)


    nla = NLAnalysisSql.NLAnalysisSql()
    sql = nla.createSparql(test_data)

    queryresult = Wikiapi.getQueryDataBySparql(sql)

    srp = SparqlResultProcess.SparqlResultProcess()
    srp.processResult(test_data, queryresult)

    print(sql)



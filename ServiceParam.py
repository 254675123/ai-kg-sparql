#!/usr/bin/python
# -*- coding: UTF-8 -*-

class ServiceParam:
    'SPARQL 查询服务项'

    # 获取指定语种服务标签字符串
    # service wikibase:label{bd:serviceParam wikibase:language "zh-cn" .}
    def getLanguageLabel(self, lang):
        "获取指定语种的服务串"
        qutation = "\""
        qutLang = qutation + lang + qutation
        prefix = "service wikibase:label{bd:serviceParam wikibase:language %s .}" % (qutLang)
        #print  prefix
        return prefix;

#    sp = getLanguageLabel("zh-cn");
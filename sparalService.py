from flask import Flask
from flask import request
from flask import jsonify, Response, json , make_response
import urllib
import json
import urllib.parse
import urllib.request
import sys
sys.path.append('./parse')

import SparqlQueryTemplate
import NLAnalysisSql
import SparqlResultProcess
from parse import Parse

app = Flask("my sparal service")


class MySparql:
    def __init__(self,host):
        self.host = host


    def   query(self, querystr):
        querystr = urllib.parse.quote(querystr)
        url = self.host +  '?query=' + querystr

        #for test
        #url = "http://120.26.58.228/sparql?query=1"
        request = urllib.request.Request(url)
        request.add_header('Accept', 'application/sparql-results+json')
        result = None
        try:
            result = urllib.request.urlopen(request ).read()
        except urllib.error.HTTPError:
            print("exception!")

        #print("query result: %s" % (result))
        if result is not None :
            result = result.decode()
            result = json.loads(result)
        return result

    def query_rule(self, sentence):
        #query_analyser = intelligentDrawing.BasedQueryAnalyser()
        parse = Parse()
        result = parse.parse(sentence)
        #result = parse.parseByRule(sentence)

        return result

@app.route('/query', methods=['GET', 'POST'])
def index():
    #querystr is the user query string

    # 初始化
    mysql = MySparql("http://120.26.58.228/sparql")

    # 接收自然语言
    querystr = request.args.get('query', None)

    # 自然语言解析
    query_rules = mysql.query_rule(querystr)

    # # 解析结果在图谱中对应
    # sqt = SparqlQueryTemplate.SparqlQueryTemplate()
    # spastr = sqt.receiveInputData(query_rules, 1)

    # 创建生成sql语句对象
    nlas = NLAnalysisSql.NLAnalysisSql()
    input_data = nlas.jsonprocess(query_rules)
    spastr = nlas.createSparql(query_rules)

    queryresult = mysql.query(spastr)

    # 创建查询结果处理对象
    srp = SparqlResultProcess.SparqlResultProcess()
    queryresult = srp.processResult(query_rules, queryresult)
    queryresult = srp.processHeads(nlas.head_dict, queryresult)

    print("over.")
    response = make_response(jsonify(ok=True, data=queryresult, parse = input_data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
    #return jsonify(ok=True, data=queryresult)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

